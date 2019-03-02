from card import *
from player import Player
from round import Round

cards=[]
players=[]

if __name__ == "__main__":

    l1=[e.value for e in CardValue]
    l2=[e.value for e in Suit]
    for  el1 in l1:
        for el2 in l2:
                cards.append(Card(el1,el2))
    player1=Player("arti",cards)
    player2=Player("papa",cards)
    player3=Player("mama",cards)
    players.append(player1)
    players.append(player2)
    players.append(player3)
    score = {}
    for player in players:
        score[player]=0
    barrel=False
    onBarrel=None
    barrelCounter=0
    gameEnd=False
    for i in range(100):
        currentPlayers=[]
        for j in range(3):
            currentPlayers.append(players[(i+j)%3])
        round = Round( currentPlayers, cards,barrel,onBarrel)
        res=round.runRound()
        for player in players:
            score[player] += res[player]

            if score[player]>=1000 and player==onBarrel:
                print "Congratulations "+"player "+player.getName()+" won"
                gameEnd=True
                break
            if score[player]>=880:
                score[player]=880
                if not barrel:
                    barrel=True
                    onBarrel=player
            if barrel and  player==onBarrel and score[player]<880:
                barrel = False
                onBarrel = None
                barrelCounter=0
            elif barrel and  player==onBarrel and barrelCounter>=3:
                score[player] -=120
                barrel = False
                onBarrel = None
                barrelCounter = 0
        if gameEnd:
            break
        if barrel:
            barrelCounter+=1
        else:
            for player in players:
                if score[player]>=880:
                    barrel=True
                    onBarrel=player
                    barrelCounter=1
                    break





