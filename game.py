from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        shown_dealer = ["??"] if hide else [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def _resolve_round(self, player, dealer, player_natural=False,
                       dealer_natural=False):
        self.show(player, dealer, hide=False)
        player_value, dealer_value = hand_value(player), hand_value(dealer)

        if player_natural and dealer_natural:
            print("Push.")
        elif player_natural:
            self.chips += 10
            print("Player wins.")
        elif dealer_natural or player_value > 21:
            self.chips -= 10
            print("Dealer wins.")
        elif dealer_value > 21 or player_value > dealer_value:
            self.chips += 10
            print("Player wins.")
        elif player_value < dealer_value:
            self.chips -= 10
            print("Dealer wins.")
        else:
            print("Push.")

    def round(self):
        deck = Deck()
        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]
        self.show(player, dealer)

        player_natural = len(player) == 2 and hand_value(player) == 21
        dealer_natural = len(dealer) == 2 and hand_value(dealer) == 21
        if player_natural or dealer_natural:
            self._resolve_round(player, dealer, player_natural, dealer_natural)
            return True

        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()
            if key == "q":
                return False
            if key == "s":
                break
            if key == "h":
                player.append(deck.draw())
                self.show(player, dealer)
                if hand_value(player) > 21:
                    print("Bust.")
                    self._resolve_round(player, dealer)
                    return True
        while hand_value(dealer) < 17:
            dealer.append(deck.draw())

        self._resolve_round(player, dealer)
        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)
        while self.chips > 0:
            if not self.round():
                return
            if input("Play again? [y/n]: ").strip().lower() != "y":
                return
