from click import secho
from sys import exit

def error(message):
    secho(message, fg='red')
    exit(1)
