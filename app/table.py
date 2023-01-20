from os import system, name


def setup_table(headers: list) -> str:
    table = '|'
    for header in headers:
        table += f" {header} |"
    # Table header setup
    table += '\n'

    table += "|"
    for header in headers:
        table += f" {'-' * len(header)} |"

    return table

def add_and_print(table, data, message=""):
    table += data
    print_table(table, message)
    return table

def print_table(table, message=""):
    system('cls' if name == 'nt' else 'clear')
    print(table)
    print()
    if message:
        print(message)

