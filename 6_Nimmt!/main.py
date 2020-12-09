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

START_POINTS = 66


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

    def on_pick_row(self) -> int:
        return 1

    def on_turn_cards(self, card_by_player_id: Dict[int, int]):
        pass


class Game:
    """
    Game manager.
    """

    def __init__(self, players: List[Player]):
        # General
        self.players_by_id: Dict[int, Player] = {i: player for i, player in enumerate(players)}
        self.player_amount = len(players)

        # Overall
        self.score_by_player_id: Dict[int, int] = {i: START_POINTS for i in self.players_by_id}

        # Single round
        self.hand_cards_by_player_id = {i: [] for i in self.players_by_id}

        self.turn_cards_by_player_id = {}

        self.cards_on_table = {1: [], 2: [], 3: [], 4: []}

    def _find_row_for_card(self, card: int) -> int:

        pass

    def _add_card_to_row(self, player_id: int, card: int, row: int):
        pass

    def _add_cards_to_table(self, cards_by_player_id: Dict[int, int]):
        s = {k: v for k, v in sorted(cards_by_player_id.items(), key=lambda item: item[1])}
        for player_id, card in s.items():
            print(player_id, card, self.cards_on_table)
            row = self._find_row_for_card(card)
            self._add_card_to_row(player_id, card, row)

    def run_single_round(self) -> Dict[int, int]:
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

        # Run the game turns
        for i in range(10):
            print(f"Turn {i}")
            played_card_by_player_id = {}
            for player_id, player in self.players_by_id.items():
                played_card_by_player_id[player_id] = player.on_get_next_card()
            print(played_card_by_player_id)

        print(remaining_cards)

        return {}

    def run(self):
        while 0 < min(self.score_by_player_id.values()):
            self.run_single_round()

        print(f"Game ended, final scoring: {self.score_by_player_id}")


def main():
    players = [Player(i) for i in range(10)]

    game = Game(players)

    game.run()


if __name__ == "__main__":
    main()
