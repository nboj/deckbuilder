import base64
from typing import Union

class DeckEncoderDecoder: 
    def __init__(self, token: Union[bytes, None] = None, deck: Union[dict, None] = None):
        self.deck = deck
        self.token = token
        self._DELIMITER1 = '+'
        self._DELIMITER2= ','
        self._DELIMITER3= ';'

    def encode(self):
        if not self.deck:
            raise Exception('No deck found.')

        normal:list = self.deck['normal'].items()
        tc:list = self.deck['tc'].items()
        items:list = self.deck['item'].items()

        deck_final = ""
        for item in normal:
            deck_final+=str(item[0])+self._DELIMITER1+str(item[1])+self._DELIMITER2
        if len(normal)==0:
            deck_final+='N'
        else:
            deck_final = deck_final[:-1]

        deck_final+=self._DELIMITER3
        for item in tc:
            deck_final+=str(item[0])+self._DELIMITER1+str(item[1])+self._DELIMITER2
        if len(tc)<=0:
            deck_final+="N"
        else:
            deck_final = deck_final[:-1]

        deck_final+=self._DELIMITER3
        for item in items:
            deck_final+=str(item[0])+self._DELIMITER1+str(item[1])+self._DELIMITER2
        if len(items)<=0:
            deck_final+="N"
        else:
            deck_final = deck_final[:-1]

        print(deck_final)
        self.token = base64.b64encode(deck_final.encode("utf-8"))
        return self.token

    def decode(self):
        if not self.token:
            raise Exception('No token found.')
        new_deck = {}
        deck_final = base64.b64decode(self.token).decode("utf-8")
        final_split = deck_final.split(self._DELIMITER3)
        normal = []
        tc = []
        items = []
        if final_split[0]!="N":
            normal = final_split[0].split(self._DELIMITER2)
        if final_split[1]!="N":
            tc = final_split[1].split(self._DELIMITER2)
        if final_split[2]!="N":
            items = final_split[2].split(self._DELIMITER2)

        new_deck['normal'] = {}
        new_deck['tc'] = {}
        new_deck['item'] = {}
        for item in normal:
            sub_items = item.split(self._DELIMITER1)
            new_deck['normal'][sub_items[0]] = int(sub_items[1])
        for item in tc:
            sub_items = item.split(self._DELIMITER1)
            new_deck['tc'][sub_items[0]] = int(sub_items[1])
        for item in items:
            sub_items = item.split(self._DELIMITER1)
            new_deck['item'][sub_items[0]] = int(sub_items[1])
        self.deck = new_deck
        return new_deck
