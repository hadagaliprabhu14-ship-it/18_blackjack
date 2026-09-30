from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = ["??"] if hide else [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def _get_wager(self):
        while True:
            try:
                wager = int(input(f"Enter wager (1-{self.chips}): ").strip())
            except ValueError:
                print("Wager must be a whole number.")
                continue
            if 0 < wager <= self.chips:
                return wager
            print(f"Wager must be between 1 and {self.chips}.")

    def _draw_card(self, deck, hand, owner):
        card = deck.draw()
        if card is None:
            print("Deck is empty. Round canceled; bankroll unchanged.")
            return False

        hand.append(card)
        if owner == "Dealer":
            print("Dealer draws a card.")
        else:
            print(f"Player draws {card[0]}{card[1]}.")
        return True

    def _resolve_round(self, player, dealer, wager, player_natural=False,
                       dealer_natural=False):
        self.show(player, dealer, hide=False)
        player_value, dealer_value = hand_value(player), hand_value(dealer)

        if player_natural and dealer_natural:
            print("Push: both have blackjack.")
        elif player_natural:
            self.chips += wager
            print("Player wins with blackjack.")
        elif dealer_natural:
            self.chips -= wager
            print("Dealer wins with blackjack.")
        elif player_value > 21:
            self.chips -= wager
            print("Player busts. Dealer wins.")
        elif dealer_value > 21:
            self.chips += wager
            print("Dealer busts. Player wins.")
        elif player_value > dealer_value:
            self.chips += wager
            print("Player wins.")
        elif player_value < dealer_value:
            self.chips -= wager
            print("Dealer wins.")
        else:
            print("Push.")

    def round(self):
        wager = self._get_wager()
        deck = Deck()
        player = []
        dealer = []
        for hand, owner in ((player, "Player"), (player, "Player"),
                            (dealer, "Dealer"), (dealer, "Dealer")):
            if not self._draw_card(deck, hand, owner):
                return True
        self.show(player, dealer)

        player_natural = len(player) == 2 and hand_value(player) == 21
        dealer_natural = len(dealer) == 2 and hand_value(dealer) == 21
        if player_natural or dealer_natural:
            self._resolve_round(player, dealer, wager, player_natural,
                                dealer_natural)
            return True

        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()
            if key == "q":
                return False
            if key == "s":
                break
            if key == "h":
                if not self._draw_card(deck, player, "Player"):
                    return True
                self.show(player, dealer)
                if hand_value(player) > 21:
                    self._resolve_round(player, dealer, wager)
                    return True
            else:
                print("Invalid command. Enter h, s, or q.")
        while hand_value(dealer) < 17:
            if not self._draw_card(deck, dealer, "Dealer"):
                return True

        self._resolve_round(player, dealer, wager)
        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)
        while self.chips > 0:
            if not self.round():
                return
            if input("Play again? [y/n]: ").strip().lower() != "y":
                return
