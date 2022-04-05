class ColorPrint:
    # TODO: implement descriptors for DRY coding
    import os

    os.system("color")

    ESCAPE_ANSI = "\u001b["
    RESET = "0"
    CYAN = "6"
    RED = "1"
    GREEN = "2"
    YELLOW = "3"
    BLUE = "4"
    MAGENTA = "5"
    NOFILL = "3"
    FILL = "4"

    def test(self):
        base_string = "This string should be"
        self.print_string(f"{base_string} cyan", self.CYAN)
        self.print_string(f"{base_string} red", self.RED)
        self.print_string(f"{base_string} green", self.GREEN)
        self.print_string(f"{base_string} yellow", self.YELLOW)
        self.print_string(f"{base_string} blue", self.BLUE)
        self.print_string(f"{base_string} magenta", self.MAGENTA)

    @staticmethod
    def color_select(color_constant):
        return f"\u001b[{color_constant}m"

    def color_reset(self):
        return self.color_select(self.RESET)

    @staticmethod
    def create_color_constant(fill, color_code):
        return f"{fill}{color_code}"

    def print_string(self, string_to_print, color_code, on, fill="3"):
        color_constant = self.create_color_constant(fill, color_code)
        if on:
            print(
                f"{self.color_select(color_constant)} {string_to_print} {self.color_reset()}"
            )

    def cyan(self, string_to_print, on=True):
        self.print_string(string_to_print, self.CYAN, on)

    def red(self, string_to_print, on=True):
        self.print_string(string_to_print, self.RED, on)

    def green(self, string_to_print, on=True):
        self.print_string(string_to_print, self.GREEN, on)

    def yellow(self, string_to_print, on=True):
        self.print_string(string_to_print, self.YELLOW, on)

    def blue(self, string_to_print, on=True):
        self.print_string(string_to_print, self.BLUE, on)

    def magenta(self, string_to_print, on=True):
        self.print_string(string_to_print, self.MAGENTA, on)

    def fcyan(self, string_to_print, on=True):
        self.print_string(string_to_print, self.CYAN, on, self.FILL)

    def fred(self, string_to_print, on=True):
        self.print_string(string_to_print, self.RED, on, self.FILL)

    def fgreen(self, string_to_print, on=True):
        self.print_string(string_to_print, self.GREEN, on, self.FILL)

    def fyellow(self, string_to_print, on=True):
        self.print_string(string_to_print, self.YELLOW, on, self.FILL)

    def fblue(self, string_to_print, on=True):
        self.print_string(string_to_print, self.BLUE, on, self.FILL)

    def fmagenta(self, string_to_print, on=True):
        self.print_string(string_to_print, self.MAGENTA, on, self.FILL)
