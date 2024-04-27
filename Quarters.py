import random
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    def print(self):
        print(self.number,"of",self.suit)
        
class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Diamonds", "Hearts", "Clubs", "Spades"]
        numbers = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
        for suit in suits:
            for num in numbers:
                self.cards.append(Card(suit, num))
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_players):
        hands = []
        for i in range(num_players):
            hands.append([])
        for i in range(3):
            for x in range(num_players):
                hands[x].append(self.cards.pop(0))
        return hands
        
def points(hand):
    if(hand[0].number == hand[1].number == hand[2].number):
        return 30.5
    ttl = {"Diamonds":0,"Hearts":0,"Clubs":0,"Spades":0}
    ttl[hand[0].suit] += conv(hand[0].number)
    ttl[hand[1].suit] += conv(hand[1].number)
    ttl[hand[2].suit] += conv(hand[2].number)
    return max(ttl.values())
    
def conv(num):
    if(num == "Ace"):
        return 11
    elif (num in ["Jack","Queen","King","10"]):
        return 10
    else:
        return int(num)
    
def play(hand, deck, discard):
    return 0
    
def main():
    PLAYERS = 2
    deck = Deck()
    #deck.shuffle()
    hands = deck.deal(2)
    discard = deck.cards.pop(0)
    discard.print()
    
main()
