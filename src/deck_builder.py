# NOT TO SELF: Make deck codes so users can import decks using deck codes
import math
import asyncio
from typing import TYPE_CHECKING, Optional
from wizwalker.extensions.scripting.utils import _maybe_get_named_window
from wizwalker.memory.memory_object import MemoryReadError
from wizwalker.utils import Rectangle
from wizwalker.memory.memory_objects.window import DynamicSpellListControl, DynamicDeckListControl, SpellListControlSpellEntry, DeckListControlSpellEntry
from wizwalker.memory.memory_objects.spell import DynamicGraphicalSpell
from wizwalker.memory.memory_objects import Window
from wizwalker.memory import Window
from wizwalker import Keycode

if TYPE_CHECKING:
    from wizwalker import Client


"""
async with DeckBuilder(client) as db:
    db.add(123)

# entire deck config window
--- [DeckConfigurationWindow] SpellBookPrefsPage

# toolbar parent?
---- [ControlSprite] ControlSprite

# top bar buttons
----- [toolbar] Window

# select school
------ [TabBackground] ControlSprite
------ [Cards_Fire] ControlCheckBox
------ [Cards_Ice] ControlCheckBox
------ [Cards_Storm] ControlCheckBox
------ [Cards_Myth] ControlCheckBox
------ [Cards_All] ControlCheckBox
------ [Cards_Life] ControlCheckBox
------ [RightSideTabs] Window
------- [Cards_Death] ControlCheckBox
------- [Cards_Balance] ControlCheckBox
------- [Cards_Astral] ControlCheckBox
------- [Cards_Shadow] ControlCheckBox
------- [Cards_MonsterMagic] ControlCheckBox


# other pages (unrelated)
------ [GoToTieredWindow] Window
------- [GoToTieredGlow] ControlSprite
------- [GoToTiered] ControlCheckBox
------ [GoToGardening] ControlCheckBox
------ [GoToFishing] ControlCheckBox
------ [GoToCantrips] ControlCheckBox
------ [GoToCastleMagic] ControlCheckBox
------ [GoBackToCastleMagic] ControlCheckBox
------ [GoBackToFishing] ControlCheckBox
------ [GoBackToGardening] ControlCheckBox
------ [GoBackToTieredWindow] Window
------- [GoBackToTieredGlow] ControlSprite
------- [GoBackToTiered] ControlCheckBox


# just parent window?
----- [DeckPage] Window

?
------ [PageUp] ControlButton
------ [PageDown] ControlButton

# cards to add to deck?
------ [SpellList] SpellListControl

# equip icon
------ [EquipBorder] ControlWidget

# ?
------ [InvBorder] ControlWidget

# cards given by items? (most likely)
------ [ItemSpells] DeckListControl

# ?
------ [ControlSprite] ControlSprite

# deck selection
------ [PrevDeck] ControlButton
------ [NextDeck] ControlButton

# deck name
------ [DeckName] ControlText

# equip icon?
------ [equipFist] Window

# spells added to normal deck (may also be used for tc)
------ [CardsInDeck] DeckListControl


# tc info
------ [TreasureCardCountBackground] Window
------ [TreasureCardCount] ControlText
------ [TreasureCardIcon] Window

# rename deck
------ [NewDeckName] ControlButton

# select deck
------ [EquipButton] ControlButton

# next card selection page?
------ [NextItemSpells] ControlButton
------ [PrevItemSpells] ControlButton

# help button
------ [Help] ControlButton

# clear deck (hidden on small decks; try unhiding)
------ [ClearDeckButton] ControlButton

# quick sell tc
------ [QuickSellButton] ControlButton

# ?
----- [ControlSprite] ControlSprite
------ [DeckTitle] ControlText
----- [TutorialLogBackground1] ControlSprite

# switch to tc view
----- [TreasureCardButton] ControlCheckBox


builder.add_card_by_name("unicorn", number_of_copies: int | None)
-> number_of_copies = None: add max copies 
-> raises: ValueError(already at max copies)
-> raises: ValueError(card not found)

builder.remove_card_by_name("unicorn", number_of_copies: int | None)
-> inverse

builder.add_by_predicate(pred, number_of_copies: int | None)
-> see add_card_by_name
def pred(spell: graphical spell):
    return True or False

builder.remove_by_predicate(pred, number_of_copies: int | None)
-> inverse

builder.get_deck_preset() -> dict[...]
{
    normal: {template id: number of copies},
    tc: {template id: number of copies},
    item: {template id: number of copies}
}
-> 


builder.set_deck_preset(dict[see above], ignore_failures: bool = False)
-> removes and adds cards as needed for a preset which is a dict

"""


# TODO: finish
class DeckBuilder:
    """
    async with DeckBuilder(client) as deck_builder:
        # adds two unicorns
        await deck_builder.add_by_name("Unicorn", 2)
    """
    def __init__(self, client: "Client"):
        self.client = client
        self._deck_config_window = None

    async def open(self):
        pass

    async def close(self):
        pass

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @staticmethod
    def calculate_icon_position(
            card_number: int,
            horizontal_size: int = 33,
            vertical_size: int = 33,
            number_of_rows: int = 8,
            horizontal_spacing: int = 6,
            vertical_spacing: int = 0,
    ):
        x = (horizontal_size * card_number) - (horizontal_size // 2) + (horizontal_spacing * (card_number - 1))
        y = (vertical_size * (((card_number - 1) // number_of_rows) + 1))\
            - (vertical_size // 2) + \
            (vertical_spacing * ((card_number - 1) // number_of_rows))
        return x, y

    async def open_deck_page(self) -> None:
        """
        Opens deck page
        """
        try:
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        except ValueError:
            self._deck_config_window = None

        if not self._deck_config_window:
            spellbook = await _maybe_get_named_window(self.client.root_window, "btnSpellbook")
            async with self.client.mouse_handler:
                await self.client.mouse_handler.click_window(spellbook)
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")

        deck_button = await _maybe_get_named_window(self._deck_config_window, "Deck")

        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(deck_button)

        cards_all = await _maybe_get_named_window(self._deck_config_window, "Cards_All")

        if await cards_all.is_visible():
            async with self.client.mouse_handler:
                await self.client.mouse_handler.click_window(cards_all)

    async def close_deck_page(self) -> None:
        try:
            self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        except ValueError:
            self._deck_config_window = None

        if self._deck_config_window:
            spellbook = await _maybe_get_named_window(self.client.root_window, "btnSpellbook")
            async with self.client.mouse_handler:
                await self.client.mouse_handler.click_window(spellbook)

    async def open_and_close_deck_page(self) -> None:
        spellbook = await _maybe_get_named_window(self.client.root_window, "btnSpellbook")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(spellbook)
            await self.client.mouse_handler.click_window(spellbook)
        self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")

    async def switch_card_type_window(self) -> None:
        await self.open_deck_page()
        # Above clicks all cards so we dont need to do it again
        treasure_card_button = await _maybe_get_named_window(self._deck_config_window, "TreasureCardButton")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(treasure_card_button)

    async def get_spell_list(self) -> list[SpellListControlSpellEntry]:
        spell_list_window = await _maybe_get_named_window(self._deck_config_window, "SpellList")
        spell_list_control = DynamicSpellListControl(self.client.hook_handler, await spell_list_window.read_base_address())
        list_of_spell_entries = await spell_list_control.spell_entries()
        list_of_valid_spell_entries = []
        # We are doing this to check for valid spells. Sometimes the returned value isn't valid
        for spell in list_of_spell_entries:
            try:
                graphical = await spell.graphical_spell()
                template = await graphical.spell_template()
                await template.name()
                list_of_valid_spell_entries.append(spell)
            except:
                pass
        return list_of_valid_spell_entries

    async def get_deck_count(self)->int:
        spell_slot_rect = await self.get_deck_list_rectangle()
        spell_slots = self.divide_rectangle(spell_slot_rect, 8, 8)
        min = 0
        max = 64
        idx = int(max/2)
        ever_found = False
        async with self.client.mouse_handler:
            while True:
                found = False
                await self.client.mouse_handler.set_mouse_position(*spell_slots[idx].center())
                world_view = await self.client.get_world_view_window()
                world_view_children = await world_view.children()
                for graphical_spell_window in world_view_children:
                    name = await graphical_spell_window.maybe_read_type_name()
                    if name == 'GraphicalSpellWindow':
                        found = ever_found = True
                        await asyncio.sleep(.05)
                if max-min <= 1:
                    if idx == 0 and not ever_found:
                        return 0
                    return idx+1
                if found:
                    min = idx
                else:
                    max = idx
                idx = int((max-min)/2+min)

    async def get_deck_spell_list(self) -> list[DeckListControlSpellEntry]:
        cards_in_deck_window = await _maybe_get_named_window(self.client.root_window, "CardsInDeck")
        deck_list_control = DynamicDeckListControl(self.client.hook_handler, await cards_in_deck_window.read_base_address())
        list_of_deck_spell_entries = await deck_list_control.spell_entries()
        list_of_valid_deck_spell_entries = []
        deck_count = await self.get_deck_count()
        for idx, entry in enumerate(list_of_deck_spell_entries):
            try:
                graphical = await entry.graphical_spell()
                if not graphical:
                    continue
                template = await graphical.spell_template()
                if not template:
                    continue
                if idx > deck_count-1:
                    break;
                list_of_valid_deck_spell_entries.append(entry)
            except MemoryReadError:
                pass
        return list_of_valid_deck_spell_entries
        ## We are doing this to check for valid spells. Sometimes the returned value isn't valid
        #for spell in list_of_deck_spell_entries:
        #    graphical = await spell.graphical_spell()
        #    try:
        #        template = await graphical.spell_template()
        #        valid_graphical_spell = await spell.valid_graphical_spell()
        #        # print(await template.name())
        #        if valid_graphical_spell == 0 or valid_graphical_spell == 3:
        #            if await graphical.maybe_read_type_name() == '':
        #                pass
        #    except:
        #        pass
        #    list_of_valid_deck_spell_entries.append(spell)
        #return list_of_valid_deck_spell_entries

    #async def get_deck_spell_list_for_tc_cards(self)-> list[DeckListControlSpellEntry]:
    #    cards_in_deck_window = await _maybe_get_named_window(self.client.root_window, "CardsInDeck")
    #    deck_list_control = DynamicDeckListControl(self.client.hook_handler, await cards_in_deck_window.read_base_address())
    #    list_of_deck_spell_entries = await deck_list_control.spell_entries()
    #    list_of_valid_deck_spell_entries = []
    #    current_spell_slot = 0
    #    #for spell_slot in divided_deck_rect:
    #    #    was_empty = True
    #    #    async with self.client.mouse_handler:
    #    #        await self.client.mouse_handler.set_mouse_position(*spell_slot.center())
    #    #        world_view = await self.client.get_world_view_window()
    #    #        world_view_children = await world_view.children()
    #    #        for graphical_spell_window in world_view_children:
    #    #            name = await graphical_spell_window.maybe_read_type_name()
    #    #            if name == 'GraphicalSpellWindow':
    #    #                number_of_cards_in_the_deck = number_of_cards_in_the_deck + 1
    #    #                await asyncio.sleep(.05)
    #    #                was_empty = False
    #    #        if was_empty:
    #    #            break

    #    # We are doing this to check for valid spells. Sometimes the returned value isn't valid
    #    for spell in list_of_deck_spell_entries:
    #        try:
    #            graphical = await spell.graphical_spell(); assert(graphical is not None)
    #            template = await graphical.spell_template(); assert(template is not None)
    #            valid_graphical_spell = await spell.valid_graphical_spell()
    #            # Sometimes a template returns and empty string
    #            if await template.name() == '':
    #                continue
    #            elif valid_graphical_spell == 0 or valid_graphical_spell == 3:
    #                if not await graphical.maybe_read_type_name() == '':
    #                    list_of_valid_deck_spell_entries.append(spell)
    #                    current_spell_slot = current_spell_slot + 1
    #                    # print(current_spell_slot)
    #        except MemoryReadError:
    #            print('here')
    #            pass
    #    return list_of_valid_deck_spell_entries

    async def get_item_card_list(self) -> list[DeckListControlSpellEntry]:
        # TODO - Item cards logic. This code way just copied from above
        cards_in_item_spell_window = await _maybe_get_named_window(self.client.root_window, "ItemSpells")
        item_list_control = DynamicDeckListControl(self.client.hook_handler, await cards_in_item_spell_window.read_base_address())
        list_of_item_spell_entries = await item_list_control.spell_entries()
        list_of_valid_item_spell_entries = []
        # We are doing this to check for valid spells. Sometimes the returned value isn't valid
        for spell in list_of_item_spell_entries:
            try:
                graphical = await spell.graphical_spell(); assert(graphical is not None)
                template = await graphical.spell_template(); assert(template is not None)
                valid_graphical_spell = await spell.valid_graphical_spell()
                # Sometimes a template returns and empty string
                if await template.name() == '':
                    continue
                elif valid_graphical_spell == 0 or valid_graphical_spell == 3:
                    if not await graphical.maybe_read_type_name() == '':
                        list_of_valid_item_spell_entries.append(spell)
            except:
                pass
        return list_of_valid_item_spell_entries

    async def get_item_card_count(self):
        spell_slot_rect = await self.get_item_spells_rectangle()
        spell_slots = self.divide_rectangle(spell_slot_rect, 8, 2)
        min = 0
        max = 16
        idx = int(max/2)
        ever_found = False
        async with self.client.mouse_handler:
            while True:
                found = False
                await self.client.mouse_handler.set_mouse_position(*spell_slots[idx].center())
                world_view = await self.client.get_world_view_window()
                world_view_children = await world_view.children()
                for graphical_spell_window in world_view_children:
                    name = await graphical_spell_window.maybe_read_type_name()
                    if name == 'GraphicalSpellWindow':
                        found = ever_found = True
                        await asyncio.sleep(.05)
                if max-min <= 1:
                    if idx == 0 and not ever_found:
                        return 0
                    return idx+1
                if found:
                    min = idx
                else:
                    max = idx
                idx = int((max-min)/2+min)

    async def get_active_item_card_list(self) -> list[DeckListControlSpellEntry]:
        count = await self.get_item_card_count()
        list_of_active_item_cards = []
        every_item_card = await self.get_item_card_list()
        item_spells_rect = await self.get_item_spells_rectangle()
        divided_item_spells_rect = self.divide_rectangle(item_spells_rect, columns=8, rows=2)
        item_card_window: Window = await _maybe_get_named_window(self.client.root_window, "ItemSpells")
        sprites = await item_card_window.children()
        positions:list[Rectangle] = []
        for sprite in sprites:
            rect = await sprite.scale_to_client();
            positions.append(rect)
        for index, card in enumerate(divided_item_spells_rect):
            for pos in positions:
                #print((pos.x1, pos.y1), (card.x1, card.y1))
                if abs(pos.x1 - card.x1) < 15 and abs(pos.y1 - card.y1) < 15:
                    list_of_active_item_cards.append(every_item_card[index])
        return [item for item in every_item_card if item not in list_of_active_item_cards[:count]]

        #raise Exception("here")
        #for sprite in sprites:
        #    try:
        #        print(f"{await sprite.name()}, {await sprite.offset()}, {await sprite.flags()}")
        #    except: pass
        #raise Exception("here")
        #indexes = []
        #try:
        #    for index, spell_slot in enumerate(divided_item_spells_rect):
        #        if (index > len(every_item_card)):
        #            continue
        #        async with self.client.mouse_handler:
        #            await self.client.mouse_handler.click(*spell_slot.center())
        #        await asyncio.sleep(.3)
        #        amount = await item_card_window.children()
        #        if len(amount) > len(sprites):
        #            sprites = amount
        #            indexes.append(index)
        #    for index, spell_slot in enumerate(divided_item_spells_rect):
        #        if (index > len(every_item_card)):
        #            continue
        #        async with self.client.mouse_handler:
        #            await self.client.mouse_handler.click(*spell_slot.center())
        #        await asyncio.sleep(.3)
        #    for i in indexes:
        #        list_of_active_item_cards.append(every_item_card[i])
        #except Exception as e:
        #    print(e)
        #await self.close_deck_page()
        #return list_of_active_item_cards

    async def get_graphical_spell_cards(self) -> list[DynamicGraphicalSpell]:
        # We use this to get a list of DynamicGraphicalSpell which we then pull the names from later on
        list_of_spell_entries = await self.get_spell_list()
        list_of_spell_graphicals = []
        for spell in list_of_spell_entries:
            graphical = await spell.graphical_spell()
            list_of_spell_graphicals.append(graphical)
        return list_of_spell_graphicals

    async def get_graphical_deck_cards(self) -> list[DynamicGraphicalSpell]:
        list_of_deck_spell_entries = await self.get_deck_spell_list()

        # I also think the TC card reading bug happens here
        list_of_deck_spell_graphicals = []
        for spell in list_of_deck_spell_entries:
            graphical = await spell.graphical_spell()
            try:
                template = await graphical.spell_template()
                valid_graphical_spell = await spell.valid_graphical_spell()
                if await template.name() == '':
                    continue
                elif valid_graphical_spell == 0 or valid_graphical_spell == 3:
                    if not await graphical.maybe_read_type_name() == '':
                        list_of_deck_spell_graphicals.append(graphical)
            except:
                pass
        return list_of_deck_spell_graphicals

    async def get_graphical_item_cards(self) -> list[DynamicGraphicalSpell]:
        # I also think the TC card reading bug happens here
        list_of_item_spell_graphicals = []
        for spell in list_of_item_spell_graphicals:
            graphical = await spell.graphical_spell()
            template = await graphical.spell_template()
            valid_graphical_spell = await spell.valid_graphical_spell()
            if await template.name() == '':
                continue
            elif valid_graphical_spell == 0 or valid_graphical_spell == 3:
                if not await graphical.maybe_read_type_name() == '':
                    list_of_item_spell_graphicals.append(graphical)
        return list_of_item_spell_graphicals

    async def clear_deck(self) -> None:
        clear_deck_button = await _maybe_get_named_window(self._deck_config_window, "ClearDeckButton")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(clear_deck_button)

        message_box_modal_window = await _maybe_get_named_window(self.client.root_window, "MessageBoxModalWindow")
        leftButton = await _maybe_get_named_window(message_box_modal_window, "leftButton")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(leftButton)

    async def clear_deck_tcs(self) ->    None:
        # TODO: Over clicks for safety to make sure deck is clear, maybe find better way to determine if the deck is empty
        number_of_cards = await self.get_deck_count()
        first_card_position = await self.calculate_deck_card_position(1)
        for _ in range(number_of_cards):
            async with self.client.mouse_handler:
                await self.client.mouse_handler.click(*first_card_position)
        # We run it again because it might be clicking to fast. It's fast enough that I dont care to run it again
        number_of_cards = await self.get_deck_count()
        if number_of_cards != 0:
            await self.clear_deck_tcs()
        await self.switch_card_type_window()

    async def spell_list_get_cards_with_predicate(self, pred: callable) -> list[DynamicGraphicalSpell]:
        # I know it works but I still don't understand predicates.
            """
            Return cards that match a predicate

            Args:
                pred: The predicate function
            """
            cards = []
            spell_list = await self.get_spell_list()
            for spell in spell_list:
                if await pred(spell):
                    cards.append(spell)

            return cards

    async def deck_list_get_cards_with_predicate(self, pred: callable) -> list[DynamicGraphicalSpell]:
        # I know it works but I still don't understand predicates.
            """
            Return cards that match a predicate

            Args:
                pred: The predicate function
            """
            cards = []
            spell_list = await self.get_deck_spell_list()
            for spell in spell_list:
                if await pred(spell):
                    cards.append(spell)

            return cards

    async def _pred_match_template_name(self, coro: callable, template_name: str):
        # I know it works but I still don't understand predicates.
        """
        Args:
            coro: pred function to call
            template_name: The debug name of the cards to find
        Returns: list of possibility with the name
        """

        async def _pred(card):
            graphical = await card.graphical_spell()
            template = await graphical.spell_template()
            try:
                return template_name == await template.name()
            except MemoryReadError: 
                return False

        return await coro(_pred)

    async def spell_list_match_template(self, template_name: str) -> list[SpellListControlSpellEntry]:
        # I know it works but I still don't understand predicates.
        # Leaving this up to god if it works
        return await self._pred_match_template_name(self.spell_list_get_cards_with_predicate, template_name)

    async def deck_list_match_template(self, template_name: str) -> SpellListControlSpellEntry:
        # I know it works but I still don't understand predicates.
        # Leaving this up to god if it works
        return await self._pred_match_template_name(self.deck_list_get_cards_with_predicate, template_name)

    async def set_page(self, page_number: int):
        # Write memory address value to update the card page
        spell_list_window = await _maybe_get_named_window(self._deck_config_window, "SpellList")
        spell_list_control = DynamicSpellListControl(self.client.hook_handler, await spell_list_window.read_base_address())
        await spell_list_control.write_start_index(page_number*6)

    async def get_spell_list_rectangle(self) -> Rectangle:
        # Returns the size of the window as a rectangle so we can subdivide it later
        self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        self.spell_list = await _maybe_get_named_window(self._deck_config_window, "SpellList")
        self.spell_list_scaled = await self.spell_list.scale_to_client()
        return self.spell_list_scaled

    async def get_deck_list_rectangle(self) -> Rectangle:
        # Returns the size of the window as a rectangle so we can subdivide it later
        self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        self.deck_list = await _maybe_get_named_window(self._deck_config_window, "CardsInDeck")
        self.deck_list_scaled = await self.deck_list.scale_to_client()
        return self.deck_list_scaled

    async def get_item_spells_rectangle(self) -> Rectangle:
        # Returns the size of the window as a rectangle so we can subdivide it later
        self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        self.deck_list = await _maybe_get_named_window(self._deck_config_window, "ItemSpells")
        self.deck_list_scaled = await self.deck_list.scale_to_client()
        return self.deck_list_scaled

    def divide_rectangle(self, rectangle: Rectangle, columns: int = 2, rows=3)-> list[Rectangle]:
        # This function takes a window element and subdivides it into Columns X Rows
        # We use this to divide up the CardsInDeck and SpellList windows as the
        # cards inside the windows aren't windows themselves, unfortunately.
        width = rectangle.x2 - rectangle.x1
        height = rectangle.y2 - rectangle.y1

        # Calculate the dimensions of each smaller rectangle
        sub_width = width / columns
        sub_height = height / rows

        rectangles = []

        # Generate the smaller rectangles
        for rows in range(rows):
            for column in range(columns):
                sub_x1 = int(rectangle.x1 + column * sub_width)
                sub_y1 = int(rectangle.y1 + rows * sub_height)
                sub_x2 = int(sub_x1 + sub_width)
                sub_y2 = int(sub_y1 + sub_height)

                rectangles.append(Rectangle(sub_x1, sub_y1, sub_x2, sub_y2))

        return rectangles

    async def calculate_card_position(self, card_number) -> tuple[int, int]:
        spell_list_rectangle = await self.get_spell_list_rectangle()
        rectangle_list = self.divide_rectangle(spell_list_rectangle)
        card_rectangle = rectangle_list[card_number - 1]
        return card_rectangle.center()

    async def calculate_deck_card_position(self, card_number) -> tuple[int, int]:
        spell_list_rectangle = await self.get_deck_list_rectangle()
        rectangle_list = self.divide_rectangle(spell_list_rectangle, columns=8, rows=8)
        card_rectangle = rectangle_list[card_number - 1]
        return card_rectangle.center()

    def calcuate_position_of_card_in_page(self, cards: list, name: str) -> tuple[int, int]:
        number_of_cards_per_page = 6
        index_of_card = cards.index(name) + 1 
        page_index = math.ceil(index_of_card / number_of_cards_per_page) - 1
        index = (index_of_card) % number_of_cards_per_page 
        if index == 0:
            index = 6
        return page_index, index

    async def log_user_in_and_out(self):
        await self.client.send_key(Keycode.ESC, 0.1)
        quit_button = await _maybe_get_named_window(self.client.root_window, "QuitButton")
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(quit_button)

        while True:
            try:
                play_button = await _maybe_get_named_window(self.client.root_window, "btnPlay")
                break
            except ValueError:
                pass
        async with self.client.mouse_handler:
            await self.client.mouse_handler.click_window(play_button)
        while True:
            try:
                await _maybe_get_named_window(self.client.root_window, "btnSpellbook")
                break
            except ValueError:
                pass
        print('User has logged out and logged back in')

    async def add_by_predicate(self, predicate: callable, number_of_copies: Optional[int]):
        """
        builder.add_by_predicate(pred, number_of_copies: int | None)
        -> see add_card_by_name
        def pred(spell: graphical spell):
            return True or False
        """
        pass

    async def remove_by_predicate(self, predicate: callable, number_of_copies: Optional[int]):
        pass

    async def add_by_name(self, name: str, number_of_copies: Optional[int]):
        """
        builder.add_card_by_name("unicorn", number_of_copies: int | None)
        -> number_of_copies = None: add max copies
        -> raises: ValueError(already at max copies)
        -> raises: ValueError(card not found)
        """
        cards: list[SpellListControlSpellEntry] = await self.spell_list_match_template(name)
        if len(cards) <= 0:
            raise Exception(f"Card not found: {name}")
        card = cards[0]



        if number_of_copies == None:
            number_of_copies = (await card.max_copies()) - (await card.current_copies())

        if await card.max_copies() == await card.current_copies():
            raise ValueError(f"already at max copies for {name}")
        elif await card.max_copies() < (await card.current_copies()) + (number_of_copies):
            raise ValueError(f"number of copies is greater than the card allows")

        list_of_spells = await self.get_graphical_spell_cards()
        list_of_spell_names = []
        for spell in list_of_spells:
            template = await spell.spell_template(); assert(template is not None)
            list_of_spell_names.append(await template.name())
        card_page, card_index_on_page = self.calcuate_position_of_card_in_page(list_of_spell_names, name)
        card_position_on_page = await self.calculate_card_position(card_index_on_page)
        await self.set_page(card_page)
        async with self.client.mouse_handler:
            for _ in range(number_of_copies):
                await self.client.mouse_handler.click(*card_position_on_page)
            # await asyncio.sleep(.1)

    async def remove_by_name(self, name: str, number_of_copies: Optional[int]):
        desk_list = await self.get_graphical_deck_cards()
        list_of_spell_names = []
        calcuated_copies = 0
        for spell in desk_list:
            template = await spell.spell_template()
            list_of_spell_names.append(await template.name())
            if await template.name() == name:
                calcuated_copies = calcuated_copies + 1
        if number_of_copies != calcuated_copies:
            raise ValueError(f"Trying to delete more '{name}' spells than are in the deck")
        index = list_of_spell_names.index(name)
        deck_rect = await self.get_deck_list_rectangle()
        divided_deck_rect = self.divide_rectangle(deck_rect, columns=8, rows=8)
        sign_card = divided_deck_rect[index]
        async with self.client.mouse_handler:
            for i in range(number_of_copies):
                await self.client.mouse_handler.click(*(sign_card.center()))
                await asyncio.sleep(1)

    async def parse_deck_cards(self, tc: bool = False) -> list:
        # This function w/ arg TC returns incorrect TC's
        list_of_deck_spells = await self.get_graphical_deck_cards()
        card_names = []
        for spell in list_of_deck_spells:
            template = await spell.spell_template(); assert(template is not None)
            card_name = await template.name()
            is_tc = await template.max_copies() == 999
            #if tc and not ' TC' in card_name:
            #    # If bool TC is TRUE and ' TC' is not in the template name, we dont care about this card
            #    # Since TC bool is true, we want to return cards with ' TC' in the name
            #    # Logic states that this card would be considered a normal card in the normal deck and not a TC card
            #    continue
            #elif not tc and ' TC' in card_name:
            #    # If bool tc is FALSE and ' TC' is in the template name, we dont care about this card
            #    # This means that this card IS a TC card, but we are looking for normal cards
            #    continue
            #elif card_name is None:
            #    # Sometimes valid cards return as None, so we handle these cases
            #    continue
            if not tc and is_tc: continue
            elif card_name is None: continue
            card_names.append(card_name)
        list_of_deck_spells = []
        return card_names

    async def get_deck_preset(self) -> dict:
        # get_deck_preset works but objects in memory cause artifacting with treasure cards
        """
        builder.get_deck_preset() -> dict[...]
        {
            normal: {template id: number of copies},
            tc: {template id: number of copies},
            item: {template id: number of copies}
        }
        """
        def dict_maker(_list: list):
            d = {}
            for card in _list:
                if card in d:
                    d[card] = d[card] + 1
                else:
                    d[card] = 1
            return d
        spellbook = await _maybe_get_named_window(self.client.root_window, "btnSpellbook")
        normal_cards = []
        tc_cards = []
        item_cards = []
        assert(self._deck_config_window is not None)
        # Below we are checking if deck window is already open because
        # we can't determine what page the user is on (tc/normal)
        if await self._deck_config_window.is_visible():
            async with self.client.mouse_handler:
                await self.client.mouse_handler.click_window(spellbook)
                await self.client.mouse_handler.click_window(spellbook)
        self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        normal_cards = await self.parse_deck_cards()
        # print('Deck should be clearned, only TC Cards should remain')
        await self.open_and_close_deck_page()
        await self.switch_card_type_window()
        tc_cards = await self.parse_deck_cards(True)
        #tc_cards_spell_list = await self.get_deck_spell_list_for_tc_cards()
        #for card in tc_cards_spell_list:
        #    graphical = await card.graphical_spell(); assert(graphical is not None)
        #    template = await graphical.spell_template(); assert(template is not None)
        #    card_name = await template.name()
        #    tc_cards.append(card_name)
        await self.switch_card_type_window()
        item_cards_spell_list = await self.get_active_item_card_list()
        for card in item_cards_spell_list:
            graphical = await card.graphical_spell(); assert(graphical is not None)
            template = await graphical.spell_template(); assert(template is not None)
            card_name = await template.name()
            item_cards.append(card_name)
        deck = {
            'normal': dict_maker(normal_cards),
            'tc': dict_maker(tc_cards),
            'item': dict_maker(item_cards)
        }
        return deck
        # def dict_maker(_list: list):
        #     d = {}
        #     def checkKey(dic: dict, key: str):
        #         if key in dic.keys():
        #             return True
        #         else:
        #             return False
        #
        #     for card in _list:
        #         if checkKey(d, card):
        #             d[card] = d[card] + 1
        #         else:
        #             d[card] = 1
        #     return d
        # self._deck_config_window = await _maybe_get_named_window(self.client.root_window, "DeckConfiguration")
        # if await self._deck_config_window.is_visible():
        #     await self.open_and_close_deck_page()
        # spellbook = await _maybe_get_named_window(self.client.root_window, "btnSpellbook")
        # normal_cards = []
        # tc_cards = []
        # item_cards = []
        # normal_cards = await self.parse_deck_cards()
        # await self.clear_deck()
        # # We sleep to let memory clear out spell_list in CardsInDeck
        # # Moving to quick caused memory errors
        # # Maybe increase sleep to 2 if people complain about mismatched get_deck_preset
        # await self.switch_card_type_window()
        # tc_cards = await self.parse_deck_cards(tc=True)
        # await self.switch_card_type_window()
        # deck = {
        #     'normal': dict_maker(normal_cards),
        #     'tc': dict_maker(tc_cards),
        #     'item': dict_maker(item_cards)
        # }
        # return deck

    async def set_deck_preset(self, preset: dict):
        await self.open_deck_page()
        await self.open_and_close_deck_page()
        await self.clear_deck()
        await self.switch_card_type_window()
        await self.clear_deck_tcs()
        await self.open_and_close_deck_page()
        deck_section = preset.keys()
        for section in deck_section:
            if section == "tc":
                await self.switch_card_type_window()
                for card in (preset[section]).keys():
                    await self.add_by_name(card, (preset[section])[card])

                await self.switch_card_type_window()
            elif section == "normal":
                for card in (preset[section]).keys():
                    await self.add_by_name(card, (preset[section])[card])

if __name__ == "__main__":
    pass
