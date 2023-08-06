def colored_text(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def print_colored(text, r, g, b):
    colored = colored_text(r, g, b, text)
    print(colored)

def warn(text):
    colored = colored_text(255, 255, 0, text)
    print(colored)

def error(text):
    colored = colored_text(255, 0, 0, text)
    print(colored)
