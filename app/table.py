from os import system, name

table = ""
indent = 0

def setup_table(headers: list) -> str:
    global table
    table = '|'
    for header in headers:
        table += f" {header} |"
    # Table header setup
    table += '\n'

    table += "|"
    for header in headers:
        table += f" {'-' * len(header)} |"

def add_and_print(data, message=""):
    global table
    table += data
    print_table(message)


def print_table(message=""):
    global table
    system('cls' if name == 'nt' else 'clear')
    print(table)
    print()
    if message:
        print(message)

def change_log_index(modifier):
    global indent
    indent += modifier

def log_and_print(msg):
    print_table(msg)

    with open("tmp/log.txt", "a+", encoding="UTF-8") as log:
        output = ("\t" * indent) + msg + "\n"
        log.write(output)
        if indent == 0:
            log.write("\n")


