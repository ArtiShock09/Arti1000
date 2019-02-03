from  player import Player
from card import *

class Round:


    def __init__(self,players,allcards):
        self._joker=[]
        self._players=players
        self._cards=allcards

    def giveCards(self):
        import random
        random.shuffle(self._cards)

        for i in range(21):
             self._players[i%3].addCard(self._cards[i])
        self._joker.append(self._cards[21])
        self._joker.append(self._cards[22])
        self._joker.append(self._cards[23])

    def removeCards(self):
        for i in range(21):
             self._players[i%3].removeCards()

    def giveJoker(self,player):
        for card in self._joker:
            player.addCard(card)

    def runRound(self):
        self.removeCards()
        self.giveCards()
        results={}
        for player in self._players:
            results[player]=0
        maxVal,maxPlayer= self.trade([95,95,95])
        if maxVal!=0:
            self.giveJoker(maxPlayer)
            (maxVal,card1,card2)=maxPlayer.evalAndGiveCards(maxVal)
            filteredPlayers=filter(lambda x: x!= maxPlayer, self._players)
            filteredPlayers[0].addCard(card1)
            filteredPlayers[1].addCard(card2)

            jocker=0
            takes=[]
            playingCards = []
            for i in range(8):
                if i == 0:
                    nextPlayer = maxPlayer
                else:
                    print "The first was:"+nextPlayer.getName()
                    (nextPlayer,takes) = self.whoIsNext(nextPlayer,playingCards, jocker)
                    print  "This round was won by " +nextPlayer.getName() +" who takes " + str(takes)
                    score=results.get(nextPlayer,0)
                    results[nextPlayer]=score+takes
                    print results

                playingCards = []
                for j in range(3):
                    print  "Now is move by " +nextPlayer.getName()
                    card,jocker=nextPlayer.move(playingCards)
                    playingCards.append(card)
                    nextPlayer = self.getNextPlayer(nextPlayer)
            if results[maxPlayer]>=maxVal:
                results[maxPlayer]= maxVal

            else:
                results[maxPlayer] = -maxVal


        return results


    def getNextPlayer(self,player):
        i=0
        for p in self._players:
            if p==player:
                i+=1
                i=i%3
                return self._players[i]
            i+=1

    def whoIsNext(self,firstPlayer,cards,joker):
        shift=0
        for i in range(3):
            if firstPlayer==self._players[i]:
                shift=i
                break
        if joker==None:
            leadingSuit=cards[0].getSuit()
            filteredCards = filter(lambda x: x.getSuit() == leadingSuit, cards)

        else:
            filteredCards = filter(lambda x: x.getSuit() == joker, cards)
            if len(filteredCards)==0:
                leadingSuit = cards[0].getSuit()
                filteredCards = filter(lambda x: x.getSuit() == leadingSuit, cards)

        winningCard = max(filteredCards, key=lambda p: p.getValue())
        for i in range(3):
            if cards[i] == winningCard:
                j = (i + shift) % 3
                return (self._players[j],self.getScore(cards))

    def getScore(self,cards):
        return sum(p.getValue() for p in cards)



    def trade(self,res):
        index=0
        for player in self._players:
            maxRes=max(res)
            if res[index]!=0:
                 res[index]= player.trade(maxRes)
                 if res[index]==300:
                     break
            index=index+1
        if max(res)==0:
            return 0,self._players[0]
        elif max(res)==sum(res) or max(res)==300:
            i=res.index(max(res))
            return max(res),self._players[i]
        else:
            return self.trade(res)

