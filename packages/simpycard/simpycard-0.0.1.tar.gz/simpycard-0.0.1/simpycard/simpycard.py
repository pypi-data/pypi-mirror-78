import random

class Card:
    """Class for individual card object.
    Args:
        col (str): suit or colour of card.
        val (str): value of card.
    """
    def __init__(self, val, col):
        self.val = val
        self.col = col

    def __str__(self):
        return "|" + self.val + self.col + "|"

class Deck:
    """Class for a collection of card objects.
    Args:
        cards (list): list of cards to start with.
    """
    def __init__(self, cards=[]):
        self.cards = cards

    def shuffle(self):
        """Shuffles the cards"""
        random.shuffle(self.cards)

    def addCards(self, cards):
        """Adds a list of cards to the Deck.
        Args:
            cards (list): list of cards to append
        """
        for card in cards:
            self.cards.append(card)

    def retCard(self, ind):
        """Returns card at index.
        Args:
            ind (int): index No. of card to return

        Returns:
            r (Card): the card at index
        """
        try:
            r = self.cards[ind]
        except:
            r = False
        return r

    def takeCard(self, ind):
        """Removes and returns card at the index.
        Args:
            ind (int): index No. of card to remove and return

        Returns:
            r (Card): the card at index
        """
        try:
            r = self.cards.pop(ind)
        except:
            r = False
        return r

    def __str__(self):
        s = ""
        for card in self.cards:
            s += str(card) + " "
        return s

    def __len__(self):
        return len(self.cards)

    def toList(self):
        """Returns a list of cards as strings"""
        l = []
        for card in self.cards:
            l.append(str(card))
        return l
