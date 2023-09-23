class Settings:
    __slots__ = ('MENU_Y', 'MENU_X', 'VERTICAL_SHIFT_1', 'HORIZONTAL_SHIFT_1', 'HORIZONTAL_SHIFT_2', 'SUBINTERVAL')

    def __init__(self):
        self.MENU_Y: int = 1
        self.MENU_X: int = 5
        self.VERTICAL_SHIFT_1: int = 0  # отступ сверху перед текстом
        self.HORIZONTAL_SHIFT_1: int = 3  # отступ слева перед текстом
        self.HORIZONTAL_SHIFT_2: int = 2  # отступ слева перед вариантами
        self.SUBINTERVAL: int = 0 # empty string between options


settings = Settings()