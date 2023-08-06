from colorama import Fore, Back, init

class Console(object):
    f_colors = {
        "[black]":   Fore.BLACK,
        "[/black]":  Fore.RESET,

        "[red]":     Fore.RED,
        "[/red]":    Fore.RESET,

        "[green]":   Fore.GREEN,
        "[/green]":  Fore.RESET,

        "[yellow]":  Fore.YELLOW,
        "[/yellow]": Fore.RESET,

        "[blue]":    Fore.BLUE,
        "[/blue]":   Fore.RESET,

        "[magenta]": Fore.MAGENTA,
        "[/magenta]":Fore.RESET,

        "[cyan]":    Fore.CYAN,
        "[/cyan]":   Fore.RESET,

        "[white]":   Fore.WHITE,
        "[/white]":  Fore.RESET,

        "[reset]": Fore.RESET,
        "[d]":     Fore.RESET,
    }

    b_colors = {
        "<black>":   Back.BLACK,
        "</black>":  Back.RESET,

        "<red>":     Back.RED,
        "</red>":    Back.RESET,

        "<green>":   Back.GREEN,
        "</green>":  Back.RESET,

        "<yellow>":  Back.YELLOW,
        "</yellow>": Back.RESET,

        "<blue>":    Back.BLUE,
        "</blue>":   Back.RESET,

        "<magenta>": Back.MAGENTA,
        "</magenta>":Back.RESET,

        "<cyan>":    Back.CYAN,
        "</cyan>":   Back.RESET,

        "<white>":   Back.WHITE,
        "</white>":  Back.RESET,

        "<reset>": Back.RESET,
    }

    def __init__(self):
        init()

    def handle_colors(self,_str : str):
        for fore in self.f_colors:
            _str = _str.replace(fore,self.f_colors[fore])
        for back in self.b_colors:
            _str = _str.replace(back,self.b_colors[back])

        return _str

    def print(self,_str):
        if type(_str) == str:
            _str = self.handle_colors(_str)
            print(_str)
        else:
            print(_str)