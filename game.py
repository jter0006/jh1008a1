"""
Fit 1008 Assignment 1
"""
__FILE__ = "game.py"
__author__ = "<Ter Jing Hao>"
__student_ID__ = "34857613"

from data_structures.referential_array import ArrayR
from player import Player
from card import CardColor, CardLabel, Card
from random_gen import RandomGen
from constants import Constants
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList


def generate_cards() -> ArrayR[Card]:
    """
        Method to generate the cards for the game

        Args:
            None

        Returns:
            ArrayR[Card]: The array of Card objects generated

        Complexity:
            Best Case Complexity: O(N) - Where N is the number of cards in the deck
            Worst Case Complexity: O(N) - Where N is the number of cards in the deck
    """
    list_of_cards: ArrayR[Card] = ArrayR(Constants.DECK_SIZE)
    idx: int = 0

    for color in CardColor:
        if color != CardColor.CRAZY:
            # Generate 4 sets of cards from 0 to 9 for each color
            for i in range(10):
                list_of_cards[idx] = Card(color, CardLabel(i))
                idx += 1
                list_of_cards[idx] = Card(color, CardLabel(i))
                idx += 1

            # Generate 2 of each special card for each color
            for i in range(2):
                list_of_cards[idx] = Card(color, CardLabel.SKIP)
                idx += 1
                list_of_cards[idx] = Card(color, CardLabel.REVERSE)
                idx += 1
                list_of_cards[idx] = Card(color, CardLabel.DRAW_TWO)
                idx += 1
        else:
            # Generate the crazy and crazy draw 4 cards
            for i in range(4):
                list_of_cards[idx] = Card(CardColor.CRAZY, CardLabel.CRAZY)
                idx += 1
                list_of_cards[idx] = Card(CardColor.CRAZY, CardLabel.DRAW_FOUR)
                idx += 1

    # Randomly shuffle the cards
    RandomGen.random_shuffle(list_of_cards)
    return list_of_cards


class Game:
    def __init__(self) -> None:
        """
        Method to initialize the Game object

        Args:
            self: The Game instance

        Returns:
            None

        Complexity:
            Best Case: O(1)
            Worst Case: O(1)
        """
        # Initialize game components
        self.players = ArraySortedList(Constants.MAX_PLAYERS)
        self.draw_pile = ArrayStack(Constants.DECK_SIZE)
        self.discard_pile = ArrayStack(Constants.DECK_SIZE)

        # Initialize game state variables
        self.current_player = None
        self.current_color = None
        self.current_label = None
        self.num_players = 0
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise

    def initialise_game(self, players: ArrayR[Player]) -> None:
        """
        Method to set up the game by initializing players, dealing cards, and setting up draw and discard piles

        Args:
            self: The Game instance
            players (ArrayR[Player]): Array of Player objects

        Returns:
            None

        Complexity:
            Best Case Complexity: O(D + P * C). Where D is DECK_SIZE, P is the number of players, C is NUM_CARDS_AT_INIT
            Worst Case Complexity: O(D).Where D is DECK_SIZE. O(D), P is the number of players, C is NUM_CARDS_AT_INIT
            dominated by the time required to generate, shuffle, deal cards,
            and potentially iterate through almost the entire remaining deck to find a valid starting card
            for the discard pile. Since the draw pile initially contains D - P * C cards
            O(P + D + P * C + (D - P * C)) = O(2D), which simplifies to O(D)
        """
        # Populate players
        self.num_players = 0
        for player in players:
            if player is not None:
                self.players[self.num_players] = player
                self.num_players += 1

        # Generate and shuffle cards
        cards = generate_cards()

        # Deal initial cards to players
        card_index = 0
        for _ in range(Constants.NUM_CARDS_AT_INIT):
            for player_index in range(self.num_players):
                self.players[player_index].add_card(cards[card_index])
                card_index += 1

        # Add remaining cards to draw pile
        for i in range(card_index, Constants.DECK_SIZE):
            self.draw_pile.push(cards[i])

        # Set up the discard pile with a valid starting card
        while True:
            top_card = self.draw_pile.pop()
            self.discard_pile.push(top_card)
            if top_card.label < 10:
                break

        # Set current color and label
        self.current_color = self.discard_pile.peek().color
        self.current_label = self.discard_pile.peek().label

    def draw_card(self, player: Player, playing: bool) -> Card:
        """
        Method to draw a card from the draw pile, reshuffling if necessary

        Args:
            self: The Game instance
            player (Player): The player drawing the card
            playing (bool): Whether the player is currently playing or not

        Returns:
            Card: The drawn card

        Complexity:
            Best Case: O(1) when draw pile is not empty
            Worst Case: O(N) when reshuffling is needed, where N is the number of cards in discard pile
        """
        # Check if draw pile is empty and reshuffle if necessary
        if self.draw_pile.is_empty():
            # Reshuffle discard pile into draw pile, keeping the top card
            top_card = self.discard_pile.pop()

            # Transfer cards from discard pile to a temporary ArrayR
            temp_array = ArrayR(len(self.discard_pile))
            index = 0
            while not self.discard_pile.is_empty():
                temp_array[index] = self.discard_pile.pop()
                index += 1

            # Shuffle the temporary ArrayR
            RandomGen.random_shuffle(temp_array)

            # Push shuffled cards back to draw pile
            for i in range(len(temp_array)):
                self.draw_pile.push(temp_array[i])

            # Put the top card back on the discard pile
            self.discard_pile.push(top_card)

        # Draw a card from the pile
        card = self.draw_pile.pop()

        # Add card to player's hand if not playing or can't play the card
        if not (playing and self.can_play_card(card)):
            player.add_card(card)

        return card

    def next_player(self) -> Player:
        """
        Method to determine the next player based on the current direction

        Args:
            self: The Game instance

        Returns:
            Player: The next player in the sequence

        Complexity:
            Best Case: O(1) when current player is the last in the list
            Worst Case: O(N) where N is the number of players
        """
        # If it's the first turn, return the first player
        if self.current_player is None and (self.direction == 1):
            return self.players[0]

        # Find the index of the current player
        current_index = 0
        for i in range(self.num_players):
            if self.players[i] == self.current_player:
                current_index = i
                break

        # Calculate the index of the next player
        next_index = (current_index + self.direction) % self.num_players
        return self.players[next_index]

    def play_reverse(self) -> None:
        """
        Method to reverse the direction of play

        Args:
            self: The Game instance

        Returns:
            None

        Complexity:
            Best Case: O(1)
            Worst Case: O(1)
        """
        # Reverse the direction by multiplying by -1, 1 is clockwise and -1 is anti-clockwise
        self.direction *= -1

    def play_skip(self) -> None:
        """
        Method to skip the next player in sequence

        Args:
            self: The Game instance

        Returns:
            None

        Complexity:
            Best Case: O(1)
            Worst Case: O(N), where N is the number of players (due to next_player method)
        """
        # Set the current player to the next player, effectively skipping one
        self.current_player = self.next_player()

    def crazy_play(self, card: Card) -> None:
        """
        Method to handle the play of a crazy card (wild or draw four)

        Args:
            self: The Game instance
            card (Card): The crazy card being played

        Returns:
            None

        Complexity:
            Best Case: O(1) for wild card
            Worst Case: O(N) for draw four where N is the number of cards to draw
        """
        if card.label == CardLabel.DRAW_TWO:
            # Handle draw two card
            next_player = self.next_player()
            for _ in range(2):
                self.draw_card(next_player, False)
        else:
            # Handle wild or draw four card
            self.current_color = CardColor(RandomGen.randint(0, 3))
            if card.label == CardLabel.DRAW_FOUR:
                next_player = self.next_player()
                for _ in range(4):
                    self.draw_card(next_player, False)

    def can_play_card(self, card: Card) -> bool:
        """
        Method to check if a card can be played based on the current game state

        Args:
            self: The Game instance
            card (Card): The card to check

        Returns:
            bool: True if the card can be played, False otherwise

        Complexity:
            Best Case: O(1)
            Worst Case: O(1)
        """
        # Check if the card matches the current color, label, or is a wild card
        return card.color == CardColor.CRAZY or card.color == self.current_color or card.label == self.current_label

    def check_skip_card(self) -> Player | None:
        """
        Method to check if the current player has a skip card

        Args:
            self: The Game instance

        Returns:
            Player | None: The player with a skip card, or None if no skip card is found

        Complexity:
            Best Case: O(1) if the first card is a skip card
            Worst Case: O(N), where N is the number of cards in the current player's hand
        """
        if self.current_player == CardLabel.SKIP:
            for i in range(len(self.current_player)):
                if self.current_player[i] == CardLabel.SKIP:
                    return self.current_player[i]
        return None

    def check_winner(self, played_card: Card) -> bool:
        """
        Method to check if the current player has won the game

        Args:
            self: The Game instance
            played_card (Card): The last card played

        Returns:
            bool: True if the current player has won, False otherwise

        Complexity:
            Best Case: O(1) if the player has not won
            Worst Case: O(N), where N is the number of cards to draw (in case of DRAW_TWO or DRAW_FOUR)
        """
        if len(self.current_player) == 0:
            print(f"{self.current_player.name} has no cards left!")

            # Check if the last card requires the next player to draw
            if played_card.label == CardLabel.DRAW_TWO or played_card.label == CardLabel.DRAW_FOUR:
                self.next_player()
                next_player = self.next_player()
                cards_to_draw = 2 if played_card.label == CardLabel.DRAW_TWO else 4
                print(f"{next_player.name} must draw {cards_to_draw} cards before the game ends")
                for _ in range(cards_to_draw):
                    self.draw_card(next_player, False)

            print(self.next_player())
            print(f"{self.current_player.name} wins!")
            return True
        return False

    def play_game(self) -> Player:
        """
        Method to run the main game loop that manages the flow of the UNO game

        Args:
            self: The Game instance

        Returns:
            Player: The winning player

        Complexity:
            Best Case: O(R * P), where R is the number of rounds played and P is the number of players
            Worst Case: O(R * (P + D)), where R is the number of rounds, P is the number of players,
                        and D is the deck size (due to potential reshuffling).
        """
        self.current_player = self.players[0]  # Start with the first player
        print(f"Game starts with {self.current_player.name}")
        print(f"Starting card: {self.current_color} {self.current_label}")
        round_count = 0

        while True:
            round_count += 1
            print(f"\nRound: {round_count}")
            print(f"Current player: {self.current_player.name}")
            print(f"Current card: {self.current_color} {self.current_label}")
            print(f"{self.current_player.name}'s hand: {[str(self.current_player[i]) for i in range(len(self.current_player))]}")

            # Try to play a card
            played_card = None
            for i in range(len(self.current_player)):
                card = self.current_player[i]
                if self.can_play_card(card):
                    played_card = self.current_player.play_card(i)
                    print(f"{self.current_player.name} plays {played_card}")
                    break

            if played_card is None:
                # If no card can be played, draw a card
                print(f"{self.current_player.name} cannot play, drawing a card")
                drawn_card = self.draw_card(self.current_player, True)
                print(f"Draw card: {drawn_card}")
                # Check if the drawn card can be played
                if self.can_play_card(drawn_card):
                    print(f"{self.current_player.name} draws and can play: {drawn_card}")
                    self.current_player.add_card(drawn_card)
                    # Play the drawn card if it matches the current color/label
                    for i in range(len(self.current_player)):
                        if drawn_card == self.current_player[i]:
                            played_card = self.current_player.play_card(i)
                            break
                else:
                    print(f"{self.current_player.name} draws a card and cannot play it")

            if played_card:
                # Update the discard pile and the current card details
                self.discard_pile.push(played_card)
                self.current_color = played_card.color
                self.current_label = played_card.label
                print(f"New top card: {self.current_color} {self.current_label}")

                # Handle special cards like REVERSE, SKIP, and CRAZY
                if played_card.label == CardLabel.REVERSE:
                    self.play_reverse()
                    print("Direction reversed")
                elif played_card.label == CardLabel.SKIP:
                    if len(self.current_player) != 0:
                        self.play_skip()
                        print(f"{self.current_player.name} is skipped")
                elif played_card.color == CardColor.CRAZY:
                    self._handle_crazy_card(played_card)
                elif played_card.label == CardLabel.DRAW_TWO:
                    self._handle_draw_two()
            # Check if the current player has won the game
            if self.check_winner(played_card):
                return self.current_player

            self.current_player = self.next_player()
            print(f"Turn moves to {self.current_player.name}")

    def _handle_crazy_card(self, played_card: Card) -> None:
        """
        Method to handle the effects of playing a crazy card (wild or draw four)

        Args:
            self: The Game instance
            played_card (Card): The crazy card that was played

        Returns:
            None

        Complexity:
            Best Case: O(1) for wild card
            Worst Case: O(N) for draw four where N is the number of cards to draw
        """
        if played_card.label == CardLabel.DRAW_FOUR:
            self.crazy_play(played_card)
            print(f"New color chosen: {self.current_color}")
            # Determine the next player who must draw 4 cards
            next_player = self.next_player()
            if len(self.current_player) != 0:
                print(f"{next_player.name} must draw 4 cards and skip a turn")
                # Skip the next player's turn after drawing cards
                self.current_player = self.next_player()
        elif played_card.label == CardLabel.CRAZY:
            # Handle the CRAZY card effect
            self.crazy_play(played_card)
            print(f"New color chosen: {self.current_color}")

    def _handle_draw_two(self) -> None:
        """
        Method to handle the effects of playing a draw two card

        Args:
            self: The Game instance

        Returns:
            None

        Complexity:
            Best Case: O(1)
            Worst Case: O(1)
        """
        next_player = self.next_player()
        # If the current player has not won yet
        if len(self.current_player) != 0:
            print(f"{next_player.name} must draw 2 cards and skip a turn")
            # Make the next player draw two cards and skip their turn
            self.crazy_play(Card(self.current_color, CardLabel.DRAW_TWO))
            # Move the turn to the next player after the one who skipped
            self.current_player = self.next_player()


def test_case():
    RandomGen.set_seed(123)
    Constants.NUM_CARDS_AT_INIT = 7

    players: ArrayR[Player] = ArrayR(3)
    players[0] = Player("Alice", 0)
    players[1] = Player("Bob", 1)
    players[2] = Player("Charlie", 2)
    players[3] = Player("David",3)


    g: Game = Game()
    g.initialise_game(players)
    winner: Player = g.play_game()
    print(f"Winner is {winner.name}")


if __name__ == '__main__':
    test_case()
