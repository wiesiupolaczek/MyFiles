import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.in_game = True

    def bet(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            return amount
        return 0

    def fold(self):
        self.in_game = False


class Game:
    def __init__(self):
        self.players = [
            Player("Użytkownik", 1000),
            Player("Bot 1", 1000),
            Player("Bot 2", 1000),
            Player("Bot 3", 1000),
            Player("Bot 4", 1000)
        ]
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.min_bet = 10

    def deal_hands(self):
        for _ in range(2):
            for player in self.players:
                player.hand.append(self.deck.deal())

    def deal_community_cards(self, num):
        for _ in range(num):
            self.community_cards.append(self.deck.deal())

    def betting_round(self):
        for player in self.players:
            if player.in_game:
                if player.name == "Użytkownik":
                    print(f"\nTwoja ręka: {player.hand[0]} {player.hand[1]}")
                    print(f"Twoje żetony: {player.chips}")
                    print(f"Aktualna stawka: {self.current_bet}")
                    action = input("Co chcesz zrobić? (rise/pass/fold): ").lower()
                    if action == "rise":
                        amount = int(input("O ile chcesz podnieść stawkę? "))
                        bet = player.bet(self.current_bet + amount)
                        self.pot += bet
                        self.current_bet = bet
                    elif action == "pass":
                        self.pot += player.bet(self.current_bet)
                    elif action == "fold":
                        player.fold()
                else:
                    # Prosta logika dla botów
                    if random.random() < 0.7:  # 70% szans na rise/pass
                        if random.random() < 0.3:  # 30% szans na rise
                            raise_amount = random.randint(1, 50)
                            bet = player.bet(self.current_bet + raise_amount)
                            self.pot += bet
                            self.current_bet = bet
                            print(f"{player.name} podnosi o {raise_amount}")
                        else:
                            self.pot += player.bet(self.current_bet)
                            print(f"{player.name} pasuje")
                    else:
                        player.fold()
                        print(f"{player.name} folduje")

        self.current_bet = 0

    def play_round(self):
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = self.min_bet

        # Rozdanie kart i minimalna stawka
        self.deal_hands()
        for player in self.players:
            self.pot += player.bet(self.min_bet)

        # Pre-flop
        print("\n--- Pre-flop ---")
        self.betting_round()

        # Flop
        print("\n--- Flop ---")
        self.deal_community_cards(3)
        print(f"Karty wspólne: {' '.join(str(card) for card in self.community_cards)}")
        self.betting_round()

        # Turn
        print("\n--- Turn ---")
        self.deal_community_cards(1)
        print(f"Karty wspólne: {' '.join(str(card) for card in self.community_cards)}")
        self.betting_round()

        # River
        print("\n--- River ---")
        self.deal_community_cards(1)
        print(f"Karty wspólne: {' '.join(str(card) for card in self.community_cards)}")
        self.betting_round()

        # Showdown (uproszczony)
        print("\n--- Showdown ---")
        active_players = [player for player in self.players if player.in_game]
        for player in active_players:
            print(f"{player.name}: {player.hand[0]} {player.hand[1]}")

        print(f"\nPula: {self.pot}")
        winner = random.choice(active_players)
        print(f"Zwycięzca: {winner.name}")
        winner.chips += self.pot

        # Reset statusu graczy
        for player in self.players:
            player.in_game = True
            player.hand = []


# Uruchomienie gry
game = Game()
while True:
    game.play_round()
    play_again = input("\nCzy chcesz zagrać kolejną rundę? (tak/nie): ").lower()
    if play_again != 'tak':
        break

print("\nDziękujemy za grę!")