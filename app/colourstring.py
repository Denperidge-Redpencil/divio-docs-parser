OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def colour_string(string: str, colour: str, padding: int=0) -> str:
    # Centerring after the colour definition seems to not work
    if padding > 0:
        string = string.center(padding)
    return f"{colour}{string}{ENDC}"


def ok(string: str = "OK", padding: int = 0) -> str:
    return colour_string(string, OKGREEN, padding)
    

def nok(string: str = "NOK", padding: int = 0) -> str:
    return colour_string(string, FAIL, padding)

