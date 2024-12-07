import asyncio
from src.deck_builder import DeckBuilder, MemoryReadError
from src.deck_encoder import DeckEncoderDecoder
from wizwalker import ClientHandler
from collections import namedtuple
from wizwalker.extensions.scripting.utils import _maybe_get_named_window
from wizwalker.memory.memory_objects.window import DynamicSpellListControl, DynamicDeckListControl

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
type_format_dict = {
    "char": "<c",
    "signed char": "<b",
    "unsigned char": "<B",
    "bool": "?",
    "short": "<h",
    "unsigned short": "<H",
    "int": "<i",
    "unsigned int": "<I",
    "long": "<l",
    "unsigned long": "<L",
    "long long": "<q",
    "unsigned long long": "<Q",
    "float": "<f",
    "double": "<d",
}

type_format_list = ["char", "signed char", "unsigned char", "bool", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

async def get_names(entries):
    items = []
    for entry in entries:
        try:
            graphical = await entry.graphical_spell()
            if not graphical:
                continue
            template = await graphical.spell_template()
            if not template:
                continue
            items.append(await template.name())
        except MemoryReadError:
            pass
    return items


async def main():
    async with ClientHandler() as handler:
        client = handler.get_new_clients()[0]
        print("Preparing")
        await client.activate_hooks()
        async with DeckBuilder(client) as deck_builder:
            await deck_builder.open_deck_page()
            coder = DeckEncoderDecoder()
            await deck_builder.open_deck_page()
            deck1 = await deck_builder.get_deck_preset()
            deck2 = await deck_builder.get_deck_preset()
            assert(deck1==deck2)
            print("Testing Encoder/Decoder")
            print("Deck: \n", deck1)
            coder = DeckEncoderDecoder(deck=deck1)
            token = coder.encode()
            print("Token: \n", token.decode())
            decoded_deck = coder.decode()
            print("Deck: \n", decoded_deck)
            assert(decoded_deck==deck1)
            print("Encoder/Decoder success!")

            print('Setting deck test...')
            await deck_builder.set_deck_preset(deck1)
            print('Setting deck test success!')
            print('Testing consistancy...')
            for i in range(5):
                print(f"Test {i}...")
                await deck_builder.open_deck_page()
                deck1 = await deck_builder.get_deck_preset()
                deck2 = None
                await deck_builder.open_and_close_deck_page()
                deck2 = await deck_builder.get_deck_preset()
                for (item1, item2) in zip(deck1['normal'].items(), deck2['normal'].items()):
                    if item1!=item2:
                        print('\n')
                        print(item1, item2)
                        print(deck1['normal'])
                        print(deck1['tc'])
                        print(deck1['item'])
                        print('\n')
                        print(deck2['normal'])
                        print(deck2['tc'])
                        print(deck2['item'])
                        assert(item1==item2)
                if (deck1 != deck2):
                    print('\n')
                    print(deck1['normal'])
                    print(deck1['tc'])
                    print(deck1['item'])
                    print('\n')
                    print(deck2['normal'])
                    print(deck2['tc'])
                    print(deck2['item'])
                    assert(deck1==deck2)
                print(f"Test {i} success!")
            print("Consistancy passed!")
            print("All tests passed!")

def print_deck(deck:dict):
    normal = deck['normal'].items()
    tc = deck['tc'].items()
    items = deck['item'].items()
    print("\n\n\nNORMAL\n")
    for item in normal:
        print(item)
    print("\n\n\nTC\n")
    for item in tc:
        print(item)
    print("\n\n\nITEM\n")
    for item in items:
        print(item)
if __name__ == "__main__":
    asyncio.run(main())
