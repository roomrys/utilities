class ColorPrint:
    # TODO: implement descriptors for DRY coding
    import os
    os.system('color')

    ESCAPE_ANSI = '\u001b['
    RESET = '0'
    CYAN = '36'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    MAGENTA = '35'

    def test(self):
        base_string = 'This string should be'
        self.print_string(f'{base_string} cyan', self.CYAN)
        self.print_string(f'{base_string} red', self.RED)
        self.print_string(f'{base_string} green', self.GREEN)
        self.print_string(f'{base_string} yellow', self.YELLOW)
        self.print_string(f'{base_string} blue', self.BLUE)
        self.print_string(f'{base_string} magenta', self.MAGENTA)

    def color_select(self, color_constant):
        return f'\u001b[{color_constant}m'
    
    def color_reset(self):
        return self.color_select(self.RESET)
    
    def print_string(self, string_to_print, color_constant):
        print(f'{self.color_select(color_constant)} {string_to_print} {self.color_reset()}')

    def cyan(self, string_to_print):
        self.print_string(string_to_print, self.CYAN)

    def red(self, string_to_print):
        self.print_string(string_to_print, self.RED)

    def green(self, string_to_print):
        self.print_string(string_to_print, self.GREEN)

    def yellow(self, string_to_print):
        self.print_string(string_to_print, self.YELLOW)

    def blue(self, string_to_print):
        self.print_string(string_to_print, self.BLUE)

    def magenta(self, string_to_print):
        self.print_string(string_to_print, self.MAGENTA)