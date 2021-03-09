from lib.controller.main import Main
from lib.controller.response import Response

main = Main()
main.load_accounts()
for x in main.load_data(main.account):
    print(x.body, end='%\n' if x.response_type == Response.Type.PERCENT else '\n')