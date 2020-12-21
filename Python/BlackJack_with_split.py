import time


class Card:
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
        self.points = 0

    def __repr__(self):
        return "{} of {}".format(self.value, self.suit)

    def define_points(self, points):
        self.points += points


class Deck:
    def __init__(self):
        values = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
        suits = ("Hearts", "Diamonds", "Clubs", "Spades")
        self.cards = [Card(x, y) for x in values for y in suits]
        for self.card in self.cards:
            if self.card.value in ("2", "3", "4", "5", "6", "7", "8", "9", "10"):
                points = int(self.card.value)
            elif self.card.value == "A":
                points = 11
            else:
                points = 10
            self.card.define_points(points)

    def count(self):
        return len(self.cards)

    def __repr__(self):
        return "Deck of {} cards".format(self.count())

    def _deal(self, number):
        if self.count() != 0:
            if number < self.count():
                cards = self.cards[-number:]
                self.cards = self.cards[:-number]
                return cards
            elif number >= self.count():
                cards = self.cards[-self.count():]
                self.cards = self.cards[:-self.count()]
                return cards
        else:
            raise ValueError("All cards have been dealt")

    def shuffle(self):
        import random
        if self.count() == 52:
            for i in range(0, 19):
                random.shuffle(self.cards)
        else:
            raise ValueError("Only full decks can be shuffled")

    def deal_card(self):
        return self._deal(1)

    # def deal_hand(self, number):
    #     return self._deal(number)


class Player:
    def __init__(self, name):
        self.name = name
        if self.name == "dealer":
            self.bankroll = "∞"
        else:
            self.bankroll = 1000
        self.hand = []
        self.split_hand = []
        self.points = 0
        self.split_points = 0
        self.current_bet = 0
        self.dd = False

    def __repr__(self):
        return f"{self.name.capitalize()} ({self.bankroll})"

    def get_points(self):
        self.points = 0
        for self.card in self.hand:
            if self.card.value == "A" and self.points + 11 > 21:
                self.card.points = 1
            self.points += self.card.points
        return self.points

    def get_split_points(self):
        self.split_points = 0
        for self.card in self.split_hand:
            if self.card.value == "A" and self.points + 11 > 21:
                self.card.points = 1
            self.split_points += self.card.points
        return self.split_points

    def bet(self, amount):
        while amount > self.bankroll or amount % 5 != 0 or amount == 0:
            print("WARNING! The bet is 0, too big or is not multiple of 5!")
            amount = int(input(f"{self.name.capitalize()}, how much would you like to bet?"))
        self.current_bet = amount
        return self.current_bet

    def double_down(self):
        self.current_bet = self.current_bet * 2
        self.dd = True

    def reset_bet(self):
        self.dd = False
        self.current_bet = 0


class Game:
    def __init__(self, num_of_players):
        self.num_of_players = num_of_players
        self.players = []
        self.rounds = []

    def create_players(self):
        names = []
        for i in range(1, self.num_of_players + 1):
            passed = False
            while not passed:
                name = input(f"Enter the name for the Player № " + str(i) + ":").lower()
                while name in names:
                    name = input(
                        f"""There is a player with name "{name}""" + " already. Enter another name for Player № "
                        + str(i) + ":").lower()
                passed = True
                names.append(name)
        real_players = [Player(name) for name in names]
        self.players.extend(real_players)
        self.players.append(Player("dealer"))

    def get_player(self, name):
        players_names = (self.player.name for self.player in self.players)
        if name.lower() in players_names:
            for self.player in self.players:
                if self.player.name == name.lower():
                    return self.player
        else:
            raise ValueError("There is no player with this name")

    def _remove_player(self, name):
        player_to_remove = self.get_player(name.lower())
        self.players.remove(player_to_remove)
        print(f"{player_to_remove} has left the game!")
        print('\n')

    def players_check(self):
        for self.player in self.players[:-1]:
            if self.player.bankroll <= 0:
                print(f"{self.player.name.capitalize()} is out of money!")
                self._remove_player(self.player.name)
        if len(self.players) > 1:
            return True
        else:
            return False

    def new_round(self):
        check = self.players_check()
        if check:
            current_round = len(self.rounds) + 1
            print(f"Round {current_round} starts now!")
            new_round = Round(self.players)
            new_round.start()
            check = self.players_check()
            if check:
                self.rounds.append(new_round)
                new_round.next_phase()
                new_round.end()


class Round:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.deck.shuffle()
        self.bankrolls_at_the_start = [self.player.bankroll for self.player in self.players]
        self.bankrolls_in_the_end = []

    def __repr__(self):
        keys = []
        values = list(map(lambda x, y: x - y, self.bankrolls_in_the_end, self.bankrolls_at_the_start))
        for self.player in self.players:
            keys.append(self.player.name.capitalize() + " had")
        result = str(dict(zip(keys, values)))
        return result

    @staticmethod
    def choose_action(actions):
        decision = None
        actions_list = ""
        counter = 1
        for a in actions:
            actions_list += f"{counter}.{a}\n"
            counter += 1
        while decision is None or decision not in range(1, len(actions) + 1):
            try:
                decision = int(input("Enter the number of an available action:\n" + actions_list))
            except ValueError:
                print("Please enter THE NUMBER from THE LIST of actions!")
        return decision

    def print_table(self):
        print('\n' * 100)
        for i in range(0, len(self.players) - 1):
            print(f"{self.players[i]} has {self.players[i].hand}({self.players[i].points})")
        print(f"{self.players[-1]} has [* of *, {self.players[-1].hand[1]}(??)")

    def _print_final_table(self):
        print(f"{self.player} has {self.player.hand}({self.player.points})")
        if self.player.split_hand:
            print(f"His 2nd hand: {self.player.split_hand}({self.player.split_points})")
        print(f"{self.players[-1]} has {self.players[-1].hand}({self.players[-1].points})")

    def _print_player_hand(self):
        print(
            f"You ({self.player}) have {self.player.hand}({self.player.points}). Your bet is {self.player.current_bet}")
        if self.player.split_hand:
            print(
                f"2nd hand: {self.player.split_hand}({self.player.split_points}).")

    def _hit(self, hand):
        hand.extend(self.deck.deal_card())
        self.player.get_points()
        if hand == self.player.split_hand:
            self.player.get_split_points()

    @staticmethod
    def stand():
        print("Okay. You've had enough.")
        time.sleep(3)

    def _split_cards(self):
        self.player.split_hand = [self.player.hand.pop()]
        pass

    def dealer_play(self):
        while self.players[-1].points <= 16:
            self.players[-1].hand.extend(self.deck.deal_card())
            self.players[-1].get_points()

    def start(self):
        for self.player in self.players[:-1]:
            actions = ["Bet", "Leave"]
            print(f"{self.player}, what do you want to do?")
            decision = self.choose_action(actions)
            if decision == 1:
                print("Make your bet! The minimum bet is 5 and it must be multiple of 5.")
                amount = int(input(f"{self.player}, how much would you like to bet?\n"))
                self.player.bet(amount)
            elif decision == 2:
                self.players.remove(self.player)
        if len(self.players) > 1:
            while len(self.players[0].hand) < 2:
                for self.player in self.players:
                    self._hit(self.player.hand)
                    self.player.get_points()

    def next_phase(self):
        for self.player in self.players[:-1]:
            self.print_table()
            if self.player.points == 21:
                print(f"{self.player}, seems your luck!")
                actions = ["BJ"]
            elif self.player.current_bet * 2 <= self.player.bankroll:
                actions = ["Hit", "Double Down", "Stand"]
                if self.player.hand[0].points == self.player.hand[1].points and self.player.hand[0]:
                    actions = ["Hit", "Split", "Double Down", "Stand"]
            else:
                actions = ["Hit", "Stand"]
            if actions != ["BJ"]:
                print(f"{self.player}, what do you want to do?")
                decision = self.choose_action(actions)
                action = actions[decision - 1]
                if action == "Hit":
                    actions = ["Hit", "Stand"]
                    while self.player.points < 21 and action == "Hit":
                        self._hit(self.player.hand)
                        self.player.get_points()
                        self._print_player_hand()
                        if self.player.points < 21:
                            decision = self.choose_action(actions)
                            action = actions[decision - 1]
                    self.stand()
                elif action == "Split":
                    hands = [self.player.hand]
                    if self.player.hand[0].value == "A":
                        self._split_cards()
                        hands.extend(self.player.split_hand)
                        for hand in hands:
                            self._hit(hand)
                        self._print_player_hand()
                        self.stand()
                    else:
                        self._split_cards()
                        hands.append(self.player.split_hand)
                        counter = 0
                        for hand in hands:
                            self._hit(hand)
                        actions = ["Hit", "Stand"]
                        for hand in hands:
                            self._print_player_hand()
                            print(f"{self.player}, what do you want to do?")
                            decision = self.choose_action(actions)
                            action = actions[decision - 1]
                            if counter == 0:
                                while self.player.points < 21 and action == "Hit":
                                    self._hit(hand)
                                    self.player.get_points()
                                    self._print_player_hand()
                                    if self.player.points < 21:
                                        decision = self.choose_action(actions)
                                        action = actions[decision - 1]
                                self.stand()
                            elif counter == 1:
                                while self.player.split_points < 21 and action == "Hit":
                                    self._hit(hand)
                                    self.player.get_split_points()
                                    self._print_player_hand()
                                    if self.player.split_points < 21:
                                        decision = self.choose_action(actions)
                                        action = actions[decision - 1]
                                self.stand()
                            counter += 1
                elif action == "Double Down":
                    self.player.double_down()
                    self._hit(self.player.hand)
                    self._print_player_hand()
                    self.stand()
                elif action == "Stand":
                    self._print_player_hand()
                    self.stand()
            self.dealer_play()

    def _win_check(self):
        dealer = self.players[-1]
        hands = [self.player.hand]
        if self.player.split_hand:
            hands.append(self.player.split_hand)
        counter = 0
        for hand in hands:
            if counter == 0:
                points = self.player.get_points()
            elif counter == 1:
                points = self.player.get_split_points()
            if points == 21 and dealer.points != 21:
                win = self.player.current_bet * (3 / 2)
                print(f"It's a Blackjack! Congratulations, {self.player.name.capitalize()}!")
                print(f"You won {win}!")
                self.player.bankroll += win
                self.bankrolls_in_the_end.append(self.player.bankroll)
            elif 21 > points > dealer.points or dealer.points > 21 > points:
                win = self.player.current_bet
                print(f"You won! Congratulations, {self.player.name.capitalize()}!")
                print(f"You won {win}!")
                self.player.bankroll += win
                self.bankrolls_in_the_end.append(self.player.bankroll)
            elif 21 >= dealer.points > points or points > 21:
                lose = self.player.current_bet
                print(f"Sorry, {self.player.name.capitalize()}, you're not a winner!")
                print(f"You lost {lose}!")
                self.player.bankroll -= lose
                self.bankrolls_in_the_end.append(self.player.bankroll)
            else:
                print(f"It's a tie, {self.player.name.capitalize()}! You can get your bet back!")
            counter += 1

    def end(self):
        print('\n' * 50)
        for self.player in self.players[:-1]:
            self._win_check()
            self.player.reset_bet()
            self._print_final_table()
            self.player.hand = []
            self.split_hand = []
            print('\n')
            time.sleep(5)
        self.players[-1].hand = []


game = None
num = 0
while num == 0:
    try:
        num = int(input("How many players will play?"))
        while num > 7 and True:
            try:
                num = int(input("Too many players. Maximum number of players is 6."))
            except ValueError:
                print("\n" * 50)
                print("Please, enter THE NUMBER of players!")
    except ValueError:
        print("\n" * 50)
        print("Please, enter THE NUMBER of players!")


def start_new_game(players_num):
    global game
    game = Game(players_num)
    game.create_players()
    check = game.players_check()
    while check:
        game.new_round()
        check = game.players_check()
    print("The last player has left the game! Thanks for playing!")


start_new_game(num)
