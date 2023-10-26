from tokens import TokenType
from nodos import *


class Parser:
    def __init__(self, tokens):
        # Crea un iterador para verificar todos los tokens con Next
        self.tokens = iter(tokens)
        self.Next()

    def Next(self):
        # Crea un next para verificar todos los tokens
        try:
            self.token_act = next(self.tokens)
        except StopIteration:
            self.token_act = None

    def NuevoSimbolo(self):
        # se encarga de crear un nuevo símbolo a partir del token actual, 

        token = self.token_act

        if token.type == TokenType.PARI:
            self.Next()
            res = self.Expression()

            if self.token_act.type != TokenType.PARD:
                raise Exception('Falta un parentesis derecho')

            self.Next()
            return res

        elif token.type == TokenType.LETRA:
            self.Next()
            return Letra(token.value)


    '''
    crea un nuevo operador a partir de un símbolo 
    (que puede ser una letra o una expresión regular entre paréntesis) 
    y luego aplica operadores de repetición (*, +) si están presentes.
    '''
    def NuevoOperador(self):
        res = self.NuevoSimbolo()

        while self.token_act != None and \
                (
                    self.token_act.type == TokenType.KLEENE or
                    self.token_act.type == TokenType.PLUS
                ):
            if self.token_act.type == TokenType.KLEENE:
                self.Next()
                res = Kleene(res)
            elif self.token_act.type == TokenType.PLUS:
                self.Next()
                res = Plus(res)

        return res


    '''
    construye la expresión regular principal. 
    Comienza creando un operador y luego aplica operadores de unión (.) y alternancia (|) 
    para construir la expresión más compleja.
    '''
    def Expression(self):
        res = self.NuevoOperador()

        while self.token_act != None and \
                (
                    self.token_act.type == TokenType.UNION or
                    self.token_act.type == TokenType.OR
                ):
            if self.token_act.type == TokenType.OR:
                self.Next()
                res = Or(res, self.NuevoOperador())

            elif self.token_act.type == TokenType.UNION:
                self.Next()
                res = Union(res, self.NuevoOperador())

        return res

    def Parse(self):
        if self.token_act == None:
            return None

        res = self.Expression()

        return res