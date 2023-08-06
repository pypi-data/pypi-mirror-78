from enum import Enum


class Ramo(str, Enum):
    Alcateia = 'A'
    TropaEscoteira = 'E'
    TropaSenior = 'S'
    ClaPioneiro = 'P'
    Todos = '*'
