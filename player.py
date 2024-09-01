"""
Fit 1008 Assignment 1
"""
__FILE__ = "player.py"
__author__ = "<Ter Jing Hao>"
__student_ID__ = "34857613"

from card import Card
from constants import Constants
from data_structures.array_sorted_list import ArraySortedList

class Player:
    """
    Player class to store the player details
    """
    def __init__(self, name: str, position: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (int): The position of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.name = name
        self.position = position
        self.hand = ArraySortedList(Constants.DECK_SIZE)  # Using DECK_SIZE from Constants

    def add_card(self, card: Card) -> None:
        """
        Method to add a card to the player's hand

        Args:
            card (Card): The card to be added to the player's hand

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) (adding to the end, no resize needed)
            Worst Case Complexity: O(n) shifting elements for insertion
        """
        self.hand.add(card)

    def play_card(self, index: int) -> Card:
        """
        Method to play a card from the player's hand

        Args:
            index (int): The index of the card to be played

        Returns:
            Card: The card at the given index from the player's hand

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(n)
        """
        return self.hand.delete_at_index(index)

    def __len__(self) -> int:
        """
        Method to get the number of cards in the player's hand

        Args:
            None

        Returns:
            int: The number of cards in the player's hand

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return len(self.hand)

    def __getitem__(self, index: int) -> Card:
        """
        Method to get the card at the given index from the player's hand

        Args:
            index (int): The index of the card to be fetched

        Returns:
            Card: The card at the given index from the player's hand

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.hand[index]

    def __str__(self) -> str:
        """
        String representation of the Player

        Returns:
            str: A string representation of the player

        Complexity:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
        """
        return f"Player {self.name} (position {self.position}): {[str(self.hand[i]) for i in range(len(self.hand))]}"
