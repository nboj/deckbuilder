import asyncio
from src.deck_encoder import DeckEncoderDecoder

#coder.token = 'Q29sb3NzYWwrMixHaWFudCs0LE1vbnN0cm91cysxLFBvdGVudCBUcmFwKzUsQXZlbmdpbmcgRm9zc2lsKzQsQmFuc2hlZSAtIFQwMi0gQSsyLERlYXRoIFNoaWVsZCsyLERlYXRoIFRyYXArMyxEZWF0aGJsYWRlKzEsRHJlYW0gU2hpZWxkKzIsR2FtYml0X0RlYXRoXzAyKzMsS2F0emVuc3RlaW4ncyBNb25zdGVyKzIsS2luZyBBcnRvcml1cyAtIERlYXRoKzIsUmFtcF9EZWF0aF8wMUErMixTa2VsZXRhbCBEcmFnb24rMztHYXJnYW50dWFuIFRDIEFWKzEsUG90ZW50IFRyYXAgVEMrMixQcmltb3JkaWFsIFRDKzMsU2hhcnBlbmVkIEJsYWRlIFRDKzMsU25pcGVyIFRDKzEsU3Ryb25nIFRDKzIsVW5zdG9wcGFibGUgVEMrNSxCbGFjayBDYXQgVEMrMixEYXJrIFBhY3QgVEMrMSxFbXBvd2VyIFRDKzYsTWFzcyBJbmZlY3Rpb24gVEMgS1IrMSxQYWNpZnkgVEMrMSxTY2FyYWIgRGVhdGggVEMgS1IrMSxWaXJ1bGVudCBQbGFndWUgVEMrMSxCYWxhbmNlYmxhZGUgVEMrMixMYWR5IEJsYWNraG9wZSBUQysxLFBvd2VyIE5vdmEgVEMrMSxSYSBUQysxLFNhYmVydG9vdGggVEMrMSxTY2FyYWIgLSBUMDIgLSBBIC0gVEMrMSxTY2FyYWIgVEMrMSxTdXBlcm5vdmEgVEMrMjtXYW5kLURlYXRoLTE0NSs0LFNoYWRvdyBUcmFwIC0gQW11bGV0KzI='.encode('utf-8')

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
    print("Preparing")
    deck1 = {'normal': {'Colossal': 5, 'Giant': 7, 'Monstrous': 6, 'Potent Trap': 4, 'Strong': 3, 'Vaporize': 1, 'Avenging Fossil': 3, 'Beguile': 3, 'Call of Khrulhu': 3, 'Gambit_Death_02': 9, 'GhostTouchRed_Trainable': 1, 'Mega Pacify': 1, 'Minion Death Seraph': 3, 'Poison': 3, 'Ramp_Death_02': 1, 'Skeletal Pirate - T02 - A': 6, 'Vampire': 1, 'Catalan': 2, 'Tri Blade': 1, 'Tri Trap': 1}, 'tc': {'Frost Beetle TC': 1, 'Frost Giant TC': 3, 'Frozen Armor TC': 1, 'Legion Shield TC': 1, 'Snow Serpent - T02 - B - TC': 1, 'Steal Ward TC': 2, 'Centaur TC': 1, 'Forest Lord TC': 1, 'Giant Spider TC KR': 2, 'Rebirth TC': 1, 'Regenerate TC': 2, 'Sanctuary TC': 3, 'Satyr TC': 2, 'Seraph - T02 - B - TC': 1, 'Spinysaur TC': 6, 'Spirit Armor TC': 3, 'Sprite Swarm TC KR': 1, 'Unicorn TC': 2, 'Heck Hound TC': 3, 'Steal Charm TC': 1, 'Wild Bolt TC': 2}, 'item': {'Moon Shield': 1, 'Wand-Death-145': 4, 'Shadow Trap - Amulet': 2}}
    deck1 = {"normal":{}, "tc":{}, "item":{}}
    coder = DeckEncoderDecoder(deck=deck1)
    #token = input("Paste your token: ")
    print("Encoding...")
    token = coder.encode()
    print("Token: ", token)

    print('Decoding...')
    deck2 = coder.decode()
    print(deck2)
    assert(deck1 == deck2)



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
