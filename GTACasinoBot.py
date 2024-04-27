import random
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def printCard(self):
        print(self.translateValue() + " of " + self.suit)

    def translateValue(self):
        returnValue = ""
        match self.value:
            case 1:
                returnValue = "Ace"
            case 11:
                returnValue = "Jack"
            case 12:
                returnValue = "Queen"
            case 13:
                returnValue = "King"
            case _:
                returnValue = str(self.value)
        return returnValue
    
    def suitRank(self):
        returnValue = ""
        match self.suit:
            case "Spades":
                returnValue = 1
            case "Hearts":
                returnValue = 2
            case "Diamonds":
                returnValue = 3
            case "Clubs":
                returnValue = 4
            case _:
                returnValue = 0
        return returnValue
        
class Deck:
    def __init__(self):
        self.deck = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        for suit in suits:
            for i in range(1,14):
                self.deck.append(Card(i, suit))
    
    def __init__(self, numDecks):
        self.deck = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        for k in range(numDecks):
            for suit in suits:
                for i in range(1,14):
                    self.deck.append(Card(i, suit))

    def shuffle(self):
        size = len(self.deck)
        for i in range(size-1, 0, -1):
            j = random.randint(0, i)
            temp = self.deck[i]
            self.deck[i] = self.deck[j]
            self.deck[j] = temp
    
    def printDeck(self):
        for card in self.deck:
            card.printCard()

    def deal(self):
        hand = []
        for i in range(2):
            hand.append(self.deck.pop())
        return hand

def calculate_hand_score(cards):
    card_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11
    }

    score = 0
    num_aces = 0

    for card in cards:
        if card.value != 1:
            score += card_values[card.translateValue()]
        else:
            num_aces += 1

    for _ in range(num_aces):
        if score + card_values['Ace'] > 21:
            score += 1
        else:
            score += card_values['Ace']

    if score > 21:
        score = -1
    return score

def playTillStand(hand, deck, stand):
    handScore = calculate_hand_score(hand)
    bust = False
    while not bust and handScore < stand:
        hand.append(deck.deck.pop(0))
        #print("dealer takes: ", end = "")
        #hand[len(hand)-1].printCard()
        handScore = calculate_hand_score(hand)
        if handScore == -1:
            #print("dealer Bust")
            bust = True
            break
    #print(handScore)
    return handScore

def compareHands(dealer, player):
    dealerScore = calculate_hand_score(dealer)
    playerScore = calculate_hand_score(player)
    if playerScore > dealerScore:
        return 1
    elif playerScore < dealerScore:
        return -1
    else:
        return 0

def main():
    ROUNDS = 100000
    for playerStand in range (11, 21):
        winRatio = 0
        for i in range(ROUNDS):
            deck = Deck(1)
            deck.shuffle()
            player = deck.deal()
            dealer = deck.deal()
            playTillStand(player, deck, playerStand)
            playTillStand(dealer, deck, 17)
            winRatio += compareHands(dealer, player)
        print("player stand on %d: %d" %(playerStand, winRatio))
    
    
main()