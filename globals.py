# from pympler import asizeof

class GlobalParameters:
    __slots__ = ('SELECTED_ITEM', 'MENU_LEVEL', 'USER_INPUT', 'SHOW_RESULTS', 'PAGE', 'ITEM_TO_SHOW', 'CHANNEL_ID',
                 'STATUS_MESSAGE', 'RESULTS_AMOUNT', 'VERSION')

    def __init__(self):
        self.SELECTED_ITEM: int = 0
        self.MENU_LEVEL: str = 'Main menu.'
        self.USER_INPUT: str = ''
        self.SHOW_RESULTS: int = 5
        self.PAGE: int = 1
        self.ITEM_TO_SHOW: int = 0
        self.CHANNEL_ID: str = ''
        self.STATUS_MESSAGE: str = ''
        self.RESULTS_AMOUNT: int = 0
        self.VERSION: float = 1.0

    def set_to_default(self):
        pass


gp = GlobalParameters()
# print(asizeof.asizeof(gp))
# 1216
# 352