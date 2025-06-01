import argparse
from time import sleep

from colorama import Back, Fore, Style, init
from game.api import Api
from game.board_handler import BoardHandler
from game.bot_handler import BotHandler
from game.util import *
from game.logic.base import BaseLogic

# Import GreedyLogic yang baru kamu buat
from game.logic.greedy import GreedyLogic

init()
BASE_URL = "http://localhost:3000/api"
DEFAULT_BOARD_ID = 1

# Tambahkan GreedyLogic di controllers
CONTROLLERS = {
    "Random": RandomLogic,  # pastikan RandomLogic juga di-import sebelumnya
    "Greedy": GreedyLogic,
}

# ... kode parsing argumen sama seperti sebelumnya ...

parser = argparse.ArgumentParser(description="Diamonds example bot")
group = parser.add_mutually_exclusive_group()
group.add_argument("--token", help="A bot token to use when running using an existing bot", action="store")
group.add_argument("--name", help="The name of the bot to register", action="store")
parser.add_argument("--email", help="The email of the bot to register", action="store")
parser.add_argument("--password", help="The password of the bot to register", action="store")
parser.add_argument("--team", help="The team of the bot to register", action="store")
parser.add_argument("--board", help="Id of the board to join", default=DEFAULT_BOARD_ID, action="store")
parser.add_argument("--time-factor", help="Factor to multiply delay", default=1, action="store")
parser.add_argument("--logic", help="Logic controller to use. Valid: {}".format(", ".join(list(CONTROLLERS.keys()))), action="store")
group = parser.add_argument_group("API connection")
group.add_argument("--host", action="store", default=BASE_URL, help="Default: {}".format(BASE_URL))
args = parser.parse_args()

time_factor = int(args.time_factor)
api = Api(args.host)
bot_handler = BotHandler(api)
board_handler = BoardHandler(api)

# Register bot jika token tidak ada
if not args.token:
    recovered_token = bot_handler.recover(args.email, args.password)
    args.token = recovered_token
    if not recovered_token:
        bot = bot_handler.register(args.name, args.email, args.password, args.team)
        if bot:
            print(Style.BRIGHT + "Bot registered. Token: {}".format(bot.id) + Style.RESET_ALL)
            args.token = bot.id
        else:
            print(Fore.RED + Style.BRIGHT + "Error: " + Style.RESET_ALL + "Unable to register bot")
            exit(1)

bot = bot_handler.get_my_info(args.token)
logic_controller = args.logic
if logic_controller not in CONTROLLERS:
    print(Fore.RED + Style.BRIGHT + "Error: " + Style.RESET_ALL + "Invalid logic controller")
    exit(1)

if not bot.name:
    print(Fore.RED + Style.BRIGHT + "Error: " + Style.RESET_ALL + "Bot does not exist")
    exit(1)
print(Fore.BLUE + Style.BRIGHT + "Welcome back, " + Style.RESET_ALL + bot.name)

logic_class = CONTROLLERS[logic_controller]
bot_logic: BaseLogic = logic_class()

current_board_id = int(args.board)
if not current_board_id:
    boards = board_handler.list_boards()
    for board in boards:
        success = bot_handler.join(bot.id, board.id)
        if success:
            current_board_id = board.id
            break
    if not current_board_id:
        exit()
else:
    success = bot_handler.join(bot.id, current_board_id)
    if not success:
        current_board_id = None

if not current_board_id:
    print(Fore.RED + Style.BRIGHT + "Error: " + Style.RESET_ALL + "Unable to find any boards to join")
    exit(1)

board = board_handler.get_board(current_board_id)
move_delay = board.minimum_delay_between_moves / 1000

while True:
    board_bot = board.get_bot(bot)
    if not board_bot:
        break

    delta_x, delta_y = bot_logic.next_move(board_bot, board)

    if not board.is_valid_move(board_bot.position, delta_x, delta_y):
        print(Fore.YELLOW + Style.BRIGHT + "Warn:" + Style.RESET_ALL, f"Invalid move ignored. Your move: ({delta_x},{delta_y})")
        sleep(1)
        continue

    try:
        board = bot_handler.move(bot.id, current_board_id, delta_x, delta_y)
    except Exception:
        break

    if not board:
        board = board_handler.get_board(current_board_id)

    board_bot = board.get_bot(bot)
    if not board_bot:
        break

    sleep(move_delay * time_factor)

print(Fore.BLUE + Style.BRIGHT + "Game over!" + Style.RESET_ALL)
