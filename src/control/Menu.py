from ..consts import MENU_SIZE


class Menu:
    # -------------------------------------------------------------------------
    # Creation and instance getters
    # -------------------------------------------------------------------------

    def __init__(self, size=None):
        self.size = MENU_SIZE if size == None else size

    def __new__(cls, size=None):
        # Singleton class
        if not hasattr(cls, 'instance'):
            cls.instance = super(Menu, cls).__new__(cls)
            cls.instance.__init__(size)
        return cls.instance

    @staticmethod
    def row_size():
        return Menu().size

    # -------------------------------------------------------------------------
    # Printing functions
    # -------------------------------------------------------------------------

    @staticmethod
    def get_option(title, options, left_aligned=False):
        Menu.print_options(title, options, left_aligned)
        min_value = 1
        max_value = len(options)
        while True:
            try:
                print("Choose an option:", end=" ")
                option = int(input())
                if option < min_value or option > max_value:
                    print(
                        f"Your input should be in the range [{min_value}, {max_value}].")
                else:
                    return options[option - 1]
            except ValueError:
                print(f"Your input should be an integer.")

    @staticmethod
    def print_options(title, options, left_aligned):
        largest_option = max(map(len, options))
        options = map(lambda x: enlarge(x, largest_option + 3), options)
        size = Menu.row_size() - 2

        def print_option_row(row):
            def left_align(row, size):
                return enlarge(" " + row, size)
            align = left_align if left_aligned else normalize
            print_middle_row(align(row, size))

        def print_middle_row(row):
            print("│" + normalize(row, size) + "│")

        def print_horizontal_border(position):
            if position == "top":
                left_char = "┌"
                right_char = "┐"
            elif position == "bottom":
                left_char = "└"
                right_char = "┘"
            else:
                left_char = "├"
                right_char = "┤"
            print(left_char + replicate("─", size) + right_char)

        print_horizontal_border("top")
        print_middle_row(title)
        print_horizontal_border("middle")
        for index, option in enumerate(options):
            print_option_row(f"[{index + 1}] {option}")
        print_horizontal_border("bottom")

# -----------------------------------------------------------------------------
# String util functions
# -----------------------------------------------------------------------------


def enlarge(string, size):
    string = str(string)
    remaining = size - len(string)
    return string + remaining * " "


def normalize(string, size=None):
    string = str(string)
    if size is None:
        size = MENU_SIZE
    remaining = size - len(string)
    padding_right = (size - len(string)) // 2
    padding_left = padding_right + remaining % 2
    return padding_left * " " + string + padding_right * " "


def replicate(char, size=None):
    if size is None:
        size = MENU_SIZE
    return size * char
