from card import Card,Suit,State,CardValue


class Player:
    def __init__(self,name,allcards):
        self._name=name
        self._score=0
        self._bolts=0
        self._cards=[]
        self._allcards=allcards
        self._currentMax=0
        self._history={}
        self._jocker=None

#[[c1,c2,c3]  ]
    def addCard(self,card):
        self._cards.append(card)

    def removeCards(self):
        self._cards=[]

    def setJocker(self,jocker):
        self._jocker = jocker



    def addHistory(self,takeNumber,takes,winner):
       self._history[takeNumber]=(takes,winner)

    def removeHistory(self):
        self._history = {}

    def getName(self):
        return  self._name

    def showCards(self):
        for e in self._cards:
            e.printCard()

    def hasAce(self,cards):
        return cards[0]==1

    def hasJoker(self,cards):
        return cards[2]*cards[3]==1

    def suitJoker(self,cards,suit):
        if not self.hasJoker(cards) :
            return 0
        elif suit==Suit.HEARTS:
            return 100
        elif suit==Suit.DIAMONDS:
            return 80
        elif suit==Suit.CLUBS:
            return 60
        else:
            return 40

    def checkTakes(self,cards):
        bin=""
        for card in cards:
            bin += str(card)
        dec=int(bin,2)
        thisdict = {
            63: (57,1),
            62: (45, 1),
            61: (45, 1),
            60: (36, 1),
            59: (45, 0),
            58: (36, 0),
            57: (36, 0),
            56: (34, 0),
            55: (45,0),
            54: (36, 0),
            53: (36, 0),
            52: (23, 0),
            51: (36, 0),
            50: (24, 0),
            49: (26, 0),
            48: (23, 0),
            47: (45, 1),
            46: (11, 0),
            45: (12,0),
            43: (14, 0),
            39: (15, 0)
        }
        res=thisdict.get(dec,(0,0))
        if res==(0,0) and cards[0]==1:
            res=(11,0)
        return res


    def getSuitList(self,suit):
        sortedCards = sorted(self._allcards, key=lambda x: (-x.getSuit(), -x.getValue()))
        filteredCards = filter(lambda x: x.getSuit() == suit, sortedCards)
        bitCards=[]
        sortedCardsPlayer = sorted(self._cards, key=lambda x: (-x.getSuit(), -x.getValue()))
        filteredCardsPlayer= filter(lambda x: x.getSuit() == suit, sortedCardsPlayer)
        for card in filteredCards:
            list1 = filter(lambda x: x.getValue() == card.getValue(), filteredCardsPlayer)
            if len(list1)==1:
                bitCards.append(1)
            else:
                bitCards.append(0)
        return bitCards

    def calculateAll(self,cards,suit):
        (takes,mar)=self.checkTakes(cards)
        if mar==1:
            return (takes+suit,0)
        else:
            return (takes,self.suitJoker(cards,suit))

    def eval(self):
        res=0
        hearts=self.getSuitList(Suit.HEARTS)
        diamonds=self.getSuitList(Suit.DIAMONDS)
        clubs= self.getSuitList(Suit.CLUBS)
        spades= self.getSuitList(Suit.SPADES)
        if self.hasAce(hearts) or self.hasAce(diamonds) or self.hasAce(clubs) or self.hasAce(spades):

           (takesh,marh)= self.calculateAll(hearts,Suit.HEARTS)
           (takesd,mard)= self.calculateAll(diamonds,Suit.DIAMONDS)
           (takesc,marc)=self.calculateAll(clubs,Suit.CLUBS)
           (takess, mars)= self.calculateAll(spades,Suit.SPADES)
           res+=takesc+takesd+takesh+takess+max(marc,mars,mard,marh)
        return res

    def move(self,playingCards):
        #TO DO : jocker is missing
        playingCard=None
        if len(playingCards)==0:
            sortedCards = sorted(self._cards, key=lambda x: x.getValue(),reverse=True)
            playingCard = sortedCards[0]

        else:
            leadingSuit = playingCards[0].getSuit()
            filteredCards = filter(lambda x: x.getSuit() == leadingSuit, self._cards)
            if len(filteredCards)!=0:
                sortedCards = sorted(filteredCards, key=lambda x: x.getValue())
            else:
                filteredCards = filter(lambda x: x.getSuit() == self._jocker, self._cards)
                if len(filteredCards)!=0:
                    sortedCards = sorted(filteredCards, key=lambda x: x.getValue())
                else:
                    sortedCards = sorted(self._cards, key=lambda x: x.getValue())
            playingCard = sortedCards[0]

        print "Player " + self._name +" moves with card "
        playingCard.printCard()

        self._cards.remove(playingCard)
        return (playingCard,None)




    def trade(self,min):
        res=self.eval()
        if res>=min+5:
            self._currentMax=res
            return min+5
        else:
            if self._currentMax<min:
                self._currentMax=0
                return 0
            else:
                return  self._currentMax


    def evalAndGiveCards(self,maxVal):
        sortedCards=sorted(self._cards, key=lambda x: x.getValue())
        #########################################################################
        #TO DO:eval 8 Cards
        self._cards.remove(sortedCards[0])
        self._cards.remove(sortedCards[1])
        return  (maxVal,sortedCards[0],sortedCards[1])

