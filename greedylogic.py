from game.logic.base import BaseLogic

class GreedyLogic(BaseLogic):
    def __init__(self):
        super().__init__()
        self.max_inventory = 10
        self.state = "collecting"
    
    def next_move(self, board_bot, board):
        # Cek apakah inventory hampir penuh
        if board_bot.inventory_count >= self.max_inventory:
            self.state = "returning"
        elif self.state == "returning" and board_bot.position == board_bot.base.position:
            self.state = "collecting"

        if self.state == "collecting":
            target = self.find_best_diamond(board_bot, board)
            if target:
                move = self.move_towards(board_bot.position, target.position, board)
            else:
                # Jika tidak ada diamond, diam saja atau gerak random
                move = (0, 0)
        else:
            move = self.move_towards(board_bot.position, board_bot.base.position, board)

        return move

    def find_best_diamond(self, board_bot, board):
        diamonds = board.get_diamonds()
        best_score = -1
        best_diamond = None

        for d in diamonds:
            dist = self.calculate_distance(board_bot.position, d.position)
            score = d.value / (dist + 1)  # Bobot nilai dibagi jarak
            if score > best_score:
                best_score = score
                best_diamond = d
        return best_diamond

    def calculate_distance(self, pos1, pos2):
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def move_towards(self, current_pos, target_pos, board):
        dx = target_pos.x - current_pos.x
        dy = target_pos.y - current_pos.y

        # Prioritaskan langkah horizontal jika ada jarak
        if dx != 0:
            step_x = 1 if dx > 0 else -1
            next_pos = (current_pos.x + step_x, current_pos.y)
            if not self.is_occupied(next_pos, board):
                return (step_x, 0)

        # Jika tidak bisa langkah horizontal, coba vertikal
        if dy != 0:
            step_y = 1 if dy > 0 else -1
            next_pos = (current_pos.x, current_pos.y + step_y)
            if not self.is_occupied(next_pos, board):
                return (0, step_y)

        # Jika tidak bisa ke target, diam
        return (0, 0)

    def is_occupied(self, pos, board):
        # Cek apakah posisi ditempati bot lain (hindari)
        for bot in board.bots:
            if bot.position.x == pos[0] and bot.position.y == pos[1]:
                return True
        return False
