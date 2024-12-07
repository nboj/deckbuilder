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
            token = input("Paste your token: ")
            #coder.token = 'Q29sb3NzYWwrMixHaWFudCs0LE1vbnN0cm91cysxLFBvdGVudCBUcmFwKzUsQXZlbmdpbmcgRm9zc2lsKzQsQmFuc2hlZSAtIFQwMi0gQSsyLERlYXRoIFNoaWVsZCsyLERlYXRoIFRyYXArMyxEZWF0aGJsYWRlKzEsRHJlYW0gU2hpZWxkKzIsR2FtYml0X0RlYXRoXzAyKzMsS2F0emVuc3RlaW4ncyBNb25zdGVyKzIsS2luZyBBcnRvcml1cyAtIERlYXRoKzIsUmFtcF9EZWF0aF8wMUErMixTa2VsZXRhbCBEcmFnb24rMztHYXJnYW50dWFuIFRDIEFWKzEsUG90ZW50IFRyYXAgVEMrMixQcmltb3JkaWFsIFRDKzMsU2hhcnBlbmVkIEJsYWRlIFRDKzMsU25pcGVyIFRDKzEsU3Ryb25nIFRDKzIsVW5zdG9wcGFibGUgVEMrNSxCbGFjayBDYXQgVEMrMixEYXJrIFBhY3QgVEMrMSxFbXBvd2VyIFRDKzYsTWFzcyBJbmZlY3Rpb24gVEMgS1IrMSxQYWNpZnkgVEMrMSxTY2FyYWIgRGVhdGggVEMgS1IrMSxWaXJ1bGVudCBQbGFndWUgVEMrMSxCYWxhbmNlYmxhZGUgVEMrMixMYWR5IEJsYWNraG9wZSBUQysxLFBvd2VyIE5vdmEgVEMrMSxSYSBUQysxLFNhYmVydG9vdGggVEMrMSxTY2FyYWIgLSBUMDIgLSBBIC0gVEMrMSxTY2FyYWIgVEMrMSxTdXBlcm5vdmEgVEMrMjtXYW5kLURlYXRoLTE0NSs0LFNoYWRvdyBUcmFwIC0gQW11bGV0KzI='.encode('utf-8')
            print('Decoding...')
            coder.token = token.encode("utf-8")
            deck = coder.decode()
            print("Setting deck...")
            await deck_builder.set_deck_preset(deck)



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
