"""
Fit 1008 Assignment 1
"""
__FILE__ = "card.py"
__author__ = "<Ter Jing Hao>"
__student_ID__ = "34857613"

from enum import auto, IntEnum

class CardColor(IntEnum):
    """
    Enum class for the color of the card
    """
    RED = 0
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    CRAZY = auto()

class CardLabel(IntEnum):
    """
    Enum class for the value of the card
    """
    ZERO = 0
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    CRAZY = auto()
    DRAW_FOUR = auto()

class Card:
    def __init__(self, color: CardColor, label: CardLabel) -> None:
        """
        Constructor for the Card class

        Args:
            color (CardColor): The color of the card
            label (CardLabel): The label of the card

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.color = color
        self.label = label

    def __str__(self) -> str:
        """
        String representation of the Card

        Returns:
            str: A string representation of the card

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return f"{self.color.name} {self.label.name}"

    def __lt__(self, other: 'Card') -> bool:
        """
        Less than comparison

        Args:
            other (Card): The other card to compare with

        Returns:
            bool: True if this card is less than the other card, False otherwise

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        if self.color != other.color:
            return self.color.value < other.color.value
        return self.label.value < other.label.value

    def __le__(self, other: 'Card') -> bool:
        """
        Less than or equal comparison

        Args:
            other (Card): The other card to compare with

        Returns:
            bool: True if this card is less than or equal to the other card, False otherwise

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self < other or self == other

    def __eq__(self, other: 'Card') -> bool:
        """
        Equality comparison

        Args:
            other (Card): The other card to compare with

        Returns:
            bool: True if this card is equal to the other card, False otherwise

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return self.color == other.color and self.label == other.label

    def __ne__(self, other: 'Card') -> bool:
        """
        Not equal comparison

        Args:
            other (Card): The other card to compare with

        Returns:
            bool: True if this card is not equal to the other card, False otherwise

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return not self == other

    def __gt__(self, other: 'Card') -> bool:
        """
        Greater than comparison

        Args:
            other (Card): The other card to compare with

        Returns:
            bool: True if this card is greater than the other card, False otherwise

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return not self <= other

    def __ge__(self, other: 'Card') -> bool:
        """
        Greater than or equal comparison

        Args:
            other (Card): The other card to compare with

        Returns:
            bool: True if this card is greater than or equal to the other card, False otherwise

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        return not self < other
