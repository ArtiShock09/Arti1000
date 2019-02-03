import enum


class Suit(enum.IntEnum):
    HEARTS=100
    DIAMONDS=80
    CLUBS=60
    SPADES=40

class CardValue(enum.IntEnum):
    NINE=0
    TEN=10
    QUEEN=3
    KING=4
    ACE=11
    JACK=2

class State(enum.IntEnum):
    DISP=0
    TRADE=1
    PLAY=2
    COUNT=3

class Card:

    def __init__(self,value,suit):
        self._value=value
        self._suit=suit

    def getValue(self):
        return self._value

    def getSuit(self):
        return self._suit

    def printCard(self):
        val=""
        if self._value==0:
            val="9"
        elif self._value== 2:
            val="Jack"
        elif self._value== 3:
            val="Queen"
        elif self._value == 4:
            val = "King"
        elif self._value== 10:
            val="10"
        elif self._value== 11:
            val="Ace"
        suit=""
        if self._suit==100:
            suit="Hearts"
        elif self._suit==80:
            suit="DIAMONDS"
        elif self._suit==60:
            suit="Clubs"
        elif self._suit == 40:
            suit = "Spades"


        print val+" " +suit