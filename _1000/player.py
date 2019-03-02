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
        self._historyCards=[]
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
        self._historyCards.extend(takes)

    def removeHistory(self):
        self._history = {}
        self._historyCards=[]

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

    def getSuit(self,numb):
        if numb==0:
            return  Suit.HEARTS
        elif numb==1:
            return Suit.DIAMONDS
        elif numb==2:
            return Suit.CLUBS
        else:
            return Suit.SPADES


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


    def getSuitList(self,suit,myCards):
        sortedCards = sorted(self._allcards, key=lambda x: (-x.getSuit(), -x.getValue()))
        filteredCards = filter(lambda x: x.getSuit() == suit, sortedCards)
        bitCards=[]
        sortedCardsPlayer = sorted(myCards, key=lambda x: (-x.getSuit(), -x.getValue()))
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

    def prepareEval(self,myCards):
        hearts=self.getSuitList(Suit.HEARTS,myCards)
        diamonds=self.getSuitList(Suit.DIAMONDS,myCards)
        clubs= self.getSuitList(Suit.CLUBS,myCards)
        spades= self.getSuitList(Suit.SPADES,myCards)
        return  (hearts,diamonds,clubs,spades)



    def eval(self):
        (hearts, diamonds, clubs, spades)=self.prepareEval(self._cards)
        res=0
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
        jocker=None
        if len(playingCards)==0:
            if not (self._history):
                sortedCards = sorted(self._cards, key=lambda x: x.getValue(),reverse=True)
                playingCard = sortedCards[0]
            else:
                (playingCard,jocker)=self.calculateMove()

        else:
            # check history and move with leading card if we have it
            # if we do not have move with smallest card

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
        return (playingCard,jocker)




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

    def getLeadingCards(self):
        temp=[]
        res=[]
        (heartsHist, diamondsHist, clubsHist, spadesHist)=self.prepareEval(self._historyCards)
        (heartsAll, diamondsAll, clubsAll, spadesAll)=self.prepareEval(self._allcards)
        return (self.getLeadingCard(heartsHist,Suit.HEARTS),self.getLeadingCard(diamondsHist,Suit.DIAMONDS),self.getLeadingCard(clubsHist,Suit.CLUBS),
                self.getLeadingCard(spadesHist,Suit.SPADES))

    def getLeadingCard(self,histCards,suit):
            #TO DO get max card
            i=0
            for card in histCards:
                if card==0:
                    break
                i+=1
            if i==0:
                return self.getCardFromAllCards(CardValue.ACE,suit)
            elif i==1:
                return self.getCardFromAllCards(CardValue.TEN, suit)
            elif i == 2:
                return self.getCardFromAllCards(CardValue.KING, suit)
            elif i == 3:
                return self.getCardFromAllCards(CardValue.QUEEN, suit)
            elif i == 4:
                return self.getCardFromAllCards(CardValue.JACK, suit)
            elif i == 5:
                return self.getCardFromAllCards(CardValue.NINE, suit)

    def getSuitByJocker(self,suit,heartsCard, diamondsCard, clubsCard, spadesCard):
        if suit==Suit.HEARTS:
            return heartsCard
        elif suit==Suit.DIAMONDS:
            return  diamondsCard
        elif suit == Suit.CLUBS:
            return clubsCard
        else:
            return spadesCard

    def getCardFromAllCards(self,cardValue, suit):
        for card in self._allcards:
            if card.getValue()==cardValue and card.getSuit()==suit:
                return card


    def calculateMove(self):

        (hearts, diamonds, clubs, spades)=self.prepareEval(self._cards)
        hasHearts = self.suitJoker(hearts, Suit.HEARTS)>0
        hasDiamonds = self.suitJoker(diamonds, Suit.DIAMONDS)>0
        hasClubs = self.suitJoker(clubs, Suit.CLUBS)>0
        hasSpades = self.suitJoker(spades, Suit.SPADES)>0
        (heartsCard, diamondsCard, clubsCard, spadesCard) = self.getLeadingCards()

        if self._jocker==None:

            if heartsCard in self._cards and not hasHearts:
                return heartsCard,None
            elif diamondsCard in self._cards and not hasDiamonds:
                return diamondsCard,None
            elif clubsCard in self._cards and not hasClubs:
                return clubsCard,None
            elif spadesCard in self._cards and not hasSpades:
                return spadesCard,None
            elif hasHearts:
                return  self.getCardFromAllCards(CardValue.QUEEN,Suit.HEARTS),Suit.HEARTS
            elif hasDiamonds:

                return self.getCardFromAllCards(CardValue.QUEEN, Suit.DIAMONDS), Suit.DIAMONDS
            elif hasClubs:

                return self.getCardFromAllCards(CardValue.QUEEN, Suit.CLUBS), Suit.CLUBS
            elif hasSpades:
                    return self.getCardFromAllCards(CardValue.QUEEN, Suit.SPADES), Suit.SPADES
            else:
                sortedCards = sorted(self._cards, key=lambda x: x.getValue())
                return sortedCards[0],None
        else:
            #TO DO: if we have jocker
            # if option 1: new jocker
            # option 2: history jocker and leading cards
            leadingCard=self.getSuitByJocker(self._jocker,heartsCard, diamondsCard, clubsCard, spadesCard)
            if leadingCard in self._cards:
                return  leadingCard,None
            elif hasHearts:
                    return self.getCardFromAllCards(CardValue.QUEEN, Suit.HEARTS), Suit.HEARTS
            elif hasDiamonds:
                    return self.getCardFromAllCards(CardValue.QUEEN, Suit.DIAMONDS), Suit.DIAMONDS
            elif hasClubs:
                    return self.getCardFromAllCards(CardValue.QUEEN, Suit.CLUBS), Suit.CLUBS
            elif hasSpades:
                    return self.getCardFromAllCards(CardValue.QUEEN, Suit.SPADES), Suit.SPADES
            else:
                if heartsCard in self._cards:
                    return heartsCard, None
                elif diamondsCard in self._cards:
                    return diamondsCard, None
                elif clubsCard in self._cards:
                    return clubsCard, None
                elif spadesCard in self._cards:
                    return spadesCard, None
                else:
                    sortedCards = sorted(self._cards, key=lambda x: x.getValue())
                    return sortedCards[0],None

