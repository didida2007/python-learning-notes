BLACKJACK = 21             # 21点分数
DEALER_STAND_SCORE = 17    # 庄家停牌分数

from enum import Enum

class Suite(Enum):
    """赋予每一个花色值"""
    SPADE, HEART, CLUB, DIAMOND = range(4)


class Card:
    """牌"""

    def __init__(self, suite, face):
        self.suite = suite
        self.face = face

    def __repr__(self):
        """返回牌的花色和点数"""
        suites = '♠♥♣♦'
        faces = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return f'{suites[self.suite.value]}{faces[self.face]}'


import random

class Poker:
    """扑克"""

    def __init__(self):
        self.cards = [Card(suite, face)
                      for suite in Suite
                      for face in range(1, 14)]  # 52张牌构成的列表
        self.current = 0  # 记录发牌位置的属性

    def shuffle(self):
        """洗牌"""
        self.current = 0
        random.shuffle(self.cards)

    def deal(self) -> Card:
        """发牌"""
        card = self.cards[self.current]
        self.current += 1
        return card


class Player:
    """玩家"""

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.score = []
        self.is_stand = False

    def add_upcard(self, card):
        """添明牌"""
        self.cards.append(card)
        print(f'{self.name} draws: {card}')

    def add_hole_card(self, card):
        """添暗牌"""
        self.cards.append(card)
        print(f'{self.name} draws a card')

    def calculate_hand(self):
        """计算手牌分"""
        score = [0]

        for card in self.cards:
            if card.face in range(10, 14):
                score = [num + 10 for num in score]
            elif card.face == 1:
                score = [num + 1 for num in score]
                score.append(score[-1] + 10)    # 所有项+1，添一项+11
            else:
                score = [num + card.face for num in score]

        self.score = score

    def print_hand(self):
        """打印手牌分"""
        score = ' or '.join(map(str, self.score))
        print(f"{self.name}'s deck: {self.cards}")
        print(f"{self.name}'s hand value: {score}")
        print()

    def highest_score(self) -> int:
        """"返回停牌分"""
        return max([num for num in self.score if num <= BLACKJACK])

    def print_stand_score(self):
        """打印停牌分"""
        print(f'{self.name} stands on {self.highest_score()}')
        print()

    def is_bust(self) -> bool:
        """判断是否爆牌"""
        return min(self.score) > BLACKJACK

    def is_blackjack(self) -> bool:
        """判断是否21点"""
        return len(self.cards) == 2 and self.score[-1] == BLACKJACK

    def clear_hand(self):
        """清空手牌"""
        self.cards = []
        self.score = []
        self.is_stand = False


class Blackjack:
    """游戏"""

    def __init__(self):
        self.deck = Poker()
        self.player = Player('Player1')
        self.dealer = Player('Dealer')
        self.winner = ''
        self.win_reason = ''
        self.game_over = False
        self.next_game = True

    def start_new_round(self):
        """开始新一局游戏"""
        self.__init__()
        self.deck.shuffle()
        print('A new game starts!')
        print()

    def deal_initial_cards(self):
        """发初始牌"""
        self.player.add_upcard(self.deck.deal())
        self.dealer.add_hole_card(self.deck.deal())
        self.player.add_upcard(self.deck.deal())
        self.dealer.add_upcard(self.deck.deal())
        print()

        self.player.calculate_hand()
        self.player.print_hand()
        self.dealer.calculate_hand()

        if self.determine_blackjack():
            self.determine_winner()

    def player_hit(self):
        """玩家要牌"""
        self.player.add_upcard(self.deck.deal())
        self.player.calculate_hand()
        self.player.print_hand()
        if self.determine_bust():
            self.determine_winner()

    def player_stand(self):
        """玩家停牌"""
        self.player.is_stand = True
        self.player.print_stand_score()

    def dealer_play(self):
        """庄家回合"""
        self.dealer.calculate_hand()
        self.dealer.print_hand()

        while min(self.dealer.score) < DEALER_STAND_SCORE:
            self.dealer.add_upcard(self.deck.deal())
            self.dealer.calculate_hand()
            self.dealer.print_hand()
            if self.determine_bust():
                self.determine_winner()
                break
        else:
            self.dealer.print_stand_score()
            self.compare_number()
            self.determine_winner()

    def determine_blackjack(self) -> bool:
        """是否有人blackjack"""
        dealer_blackjack = self.dealer.is_blackjack()
        player_blackjack = self.player.is_blackjack()

        if not (dealer_blackjack or player_blackjack):
            # 没人Blackjack，显示部分牌面
            print(f"Dealer's hand: [?, {self.dealer.cards[1]}]")
            print()
            return False

        # 有人Blackjack，显示完整牌面并判断胜负
        self.game_over = True
        self.win_reason = 'blackjack'

        print(f"Dealer's hand: {self.dealer.cards}")
        print(f"Player's hand: {self.player.cards}")
        print()

        if dealer_blackjack and player_blackjack:
            self.winner = 'push'
        elif dealer_blackjack:
            self.winner = 'dealer'
        else:
            self.winner = 'player'

        return True

    def determine_bust(self) -> bool:
        """是否有人爆牌"""
        dealer_bust = self.dealer.is_bust()
        player_bust = self.player.is_bust()

        if dealer_bust or player_bust:
            self.win_reason = 'bust'
            self.game_over = True
            if player_bust:
                self.winner = 'dealer'
            else:
                self.winner = 'player'
            return True
        else:
            return False

    def compare_number(self):
        """比大小"""
        dealer_score = self.dealer.highest_score()
        player_score = self.player.highest_score()
        self.win_reason = 'larger'
        self.game_over = True

        if dealer_score > player_score:
            self.winner = 'dealer'
        elif dealer_score < player_score:
            self.winner = 'player'
        else:
            self.winner = 'push'

    def determine_winner(self):
        """总赢家判断"""
        winner = self.winner
        win_reason = self.win_reason
        player_name = self.player.name
        dealer_name = self.dealer.name

        if win_reason == 'blackjack':
            if winner == 'dealer':
                print(f'{dealer_name} has blackjack! {dealer_name} wins!')
            elif winner == 'player':
                print(f'{player_name} has blackjack! {player_name} wins!')
            else:
                print(f'{dealer_name} and {player_name} have blackjack! Push!')

        elif win_reason == 'bust':
            if winner == 'dealer':
                print(f'{player_name} busts! {dealer_name} wins!')
            else:
                print(f'{dealer_name} busts! {player_name} wins!')

        elif win_reason == 'larger':
            if winner == 'dealer':
                print(f'{dealer_name} has a larger hand! {dealer_name} wins!')
            elif winner == 'player':
                print(f'{player_name} has a larger hand! {player_name} wins!')
            else:
                print(f'{dealer_name} and {player_name} have the same hand value! Push!')

    def play_again(self):
        """是否要再玩一局"""
        print()
        while True:
            ans = input('Do you want to play again? (y/n): ').lower().strip()
            if ans in ['y', 'yes']:
                print()
                break
            elif ans in ['n', 'no']:
                self.next_game = False
                print('Thank you for playing!')
                break
            print('Invalid input. Please try again.')


def get_action() -> str:
    """返回玩家行动"""
    while True:
        action = input('Enter "hit" or "stand": ').lower().strip()
        if action in ['hit', 'h']:
            return 'hit'
        elif action in ['stand', 's']:
            return 'stand'
        print('Invalid input. Please try again.')


def main():
    game = Blackjack()

    while game.next_game:
        game.start_new_round()
        game.deal_initial_cards()

        # 玩家回合（如果没有blackjack）
        while not game.player.is_stand and not game.game_over:
            action = get_action()
            print()
            if action == 'hit':
                game.player_hit()
            else:
                game.player_stand()

        # 庄家回合（如果玩家没爆牌）
        if not game.game_over:
            game.dealer_play()

        game.player.clear_hand()
        game.dealer.clear_hand()
        game.play_again()

if __name__ == "__main__":    # 当直接运行程序时执行 main()
    main()