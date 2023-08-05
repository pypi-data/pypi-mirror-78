from sys import argv, stdout, exit
from time import sleep
from random import uniform
from os import system, name
from getopt import getopt, GetoptError

try:
    from colorama import init, Fore, Style

except ImportError as e:
    print(e)


def version():

    print("+-------------------------------------------------------------------------------+")
    print("| knock. Copyright (C) 2020 BrainDisassembly, Contact: braindisassm@gmail.com   |")
    print("| Version: 1.0.0                                                                |")
    print("|                                                                               |")
    print("| This program comes with ABSOLUTELY NO WARRANTY; for details type `show w`.    |")
    print("| This is free software, and you are welcome to redistribute it                 |")
    print("| under certain conditions; type `show c` for details.                          |")
    print("+-------------------------------------------------------------------------------+")


def usage():

    print("Usage: {0} <options>".format(argv[0]))

    print("\nOptions:")
    print("  -h: --help                           Print usage and exit")
    print("  -V: --version                        Print version information and exit")
    print("  -a: --available                      Show available colors")
    print("  -d: --delay                          Delay (default 0.6)")
    print("  -c: --color                          Use this color for knock (default green).")
    print("  -b: --bold                           Bold characters on")
    print("  -u: --upper                          All letters uppercase")
    print("  -l: --lower                          All letters lowercase")


def available():

    print("+---------------------------------------------------------------------------+")
    print("Available colors:")
    print("+---------------------------------------------------------------------------+")

    print("[~]  (red)")
    print("[~]  (green)")
    print("[~]  (yellow)")
    print("[~]  (blue)")
    print("[~]  (magenta)")
    print("[~]  (cyan)")
    print("[~]  (white)")
    print("[~]  (black)")


def white_rabbit():

    print(Fore.WHITE)

    print("          (`.         ,-,")
    print("           `\ `.    ,;' /")
    print("            \`. \ ,'/ .' ")
    print("      __     `.\ Y /.'   ")
    print("   .-'  ''--.._` ` (     ")
    print(" .'            /   `     ")
    print(",           ` '   Q '    ")
    print(",         ,   `._    \   ")
    print("|         '     `-.;_'   ")
    print("`  ;    `  ` --,.._;     ")
    print("`    ,   )   .'          ")
    print(" `._ ,  '   /_           ")
    print("    ; ,''-,;' ``-        ")
    print("     ``-..__\``--`       Follow the white rabbit.")

    print(Style.RESET_ALL)


def knock(color):

    init()

    if bold:
        print("\033[1m")

    if color == "red":
        print(Fore.RED)

    if color == "green":
        print(Fore.GREEN)

    if color == "yellow":
        print(Fore.YELLOW)

    if color == "blue":
        print(Fore.BLUE)

    if color == "magenta":
        print(Fore.MAGENTA)

    if color == "cyan":
        print(Fore.CYAN)

    if color == "white":
        print(Fore.WHITE)

    if color == "black":
        print(Fore.BLACK)

    lines = """Wake up, Neo...
The Matrix has you...
Follow the white rabbit.
Knock, knock, Neo.\n"""

    try:
        if name == "nt":
            system("cls")
        else:
            system("clear")

        for line in lines:
            if upper:
                print(line.upper(), end="")
            elif lower:
                print(line.lower(), end="")
            else:
                print(line, end="")

            if delay:
                sleep(uniform(0, delay))
                stdout.flush()

                if line == "\n":
                    if name == "nt":
                        system("cls")
                    else:
                        system("clear")

            else:
                sleep(uniform(0, 0.6))
                stdout.flush()

                if line == "\n":
                    if name == "nt":
                        system("cls")
                    else:
                        system("clear")


    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        if name == "nt":
            system("cls")
        else:
            system("clear")

        print(Style.RESET_ALL)

        exit(1)


def main():

    color = ""
    color_flag = False

    global delay
    delay = ""

    global bold
    bold = ""

    global upper
    upper = ""

    global lower
    lower = ""

    try:
        if len(argv) == 1:
            knock("green")
            exit(1)

        else:
            opts, args = getopt(argv[1:], "hVaHc:d:bul", ["help", "version", "available", "hop", "color=", "delay=", "bold", "upper", "lower"])

    except GetoptError: usage()

    else:
        try:
            for opt, arg in opts:
                if opt in ("-h", "--help"): usage(); exit(1)
                if opt in ("-V", "--version"): version(); exit(1)
                if opt in ("-a", "--available"): available(); exit(1)
                if opt in ("-H", "--hop"): white_rabbit(); exit(1)
                if opt in ("-c", "--color"): color = arg; color_flag = True
                if opt in ("-d", "--delay"): delay = float(arg); delay_flag = True
                if opt in ("-b", "--bold"): bold = True
                if opt in ("-u", "--upper"): upper = True
                if opt in ("-l", "--lower"): lower = True

            if color: knock(color)

            elif delay: knock()
            elif bold: knock()
            elif upper: knock()
            elif lower: knock()

        except UnboundLocalError:
            pass

        except ValueError:
            pass

        usage()


if __name__ == "__main__":
        main()
