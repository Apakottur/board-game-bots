#!/usr/bin/env python
import random
from abc import ABC
from typing import List, Dict

ALL_CARDS = list(range(1, 105))

CARD_POINTS = {
    7: [55],
    5: [11, 22, 33, 44, 66, 77, 88, 99],
    3: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    2: [5, 15, 25, 35, 45, 65, 75, 85, 95]
    # All rest from 1 to 104 have 1 point.
}

CARDS_PER_PLAYER = 10

MAX_POINTS = 66


class Player:
    """
    Base class for a player.
    """

    def __init__(self, player_id: int):
        self.player_id = player_id
        self.cards_in_hands = []

    def on_game_start(self, player_amount: int, dealt_cards: List[int], table_cards: Dict[int, List[int]]):
        print(player_amount, dealt_cards, table_cards)
        self.cards_in_hands = dealt_cards

    def on_get_next_card(self) -> int:
        return self.cards_in_hands.pop()

    def on_played_cards(self, card_by_player: Dict[int, int]):
        pass


class Game:
    """
    Game manager.
    """

    def __init__(self, players: List[Player]):
        # General
        self.players_by_id: Dict[int, Player] = {i: player for i, player in enumerate(players)}
        self.player_amount = len(players)

        # Single round
        self.cards_by_player_id = {i: [] for i in self.players_by_id}
        self.cards_on_table = {1: [], 2: [], 3: [], 4: []}

    def run_single_round(self):
        remaining_cards = list(ALL_CARDS)
        random.shuffle(remaining_cards)

        # Put initial 4 cards on the table.
        for row_id, row_cards in self.cards_on_table.items():
            row_cards.append(remaining_cards.pop())

        # Deal the cards to the players.
        self.cards_by_player_id = {i: [] for i in self.players_by_id}
        for p_id, p_cards in self.cards_by_player_id.items():
            new_cards = remaining_cards[:CARDS_PER_PLAYER]
            remaining_cards = remaining_cards[CARDS_PER_PLAYER:]
            p_cards.extend(new_cards)
            self.players_by_id[p_id].on_game_start(self.player_amount, new_cards, self.cards_on_table)

        print(remaining_cards)


def main():
    players = [Player(i) for i in range(10)]

    game = Game(players)

    game.run_single_round()


if __name__ == "__main__":
    main()
