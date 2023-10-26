from tokens import Token, TokenType

ABC = 'abcdefghijklmnopqrstuvwxyz01234567890.'

# Se utiliza para leer la cadena de entrada y crear tokens.
class Reader:
    def __init__(self, string: str):
        self.string = iter(string.replace(' ', '')) # Reemplazamos los espacios con nada
        self.entrada = set() #Creamos un set, para colocar todos nuestros tokens
        self.Next() #El next es para ir entre caracteres

    # Se utiliza para avanzar al siguiente carácter en la cadena.
    def Next(self):
        try:
            self.car_actual = next(self.string)
        except StopIteration:
            self.car_actual = None

    def crearTokens(self):
        while self.car_actual != None:

            if self.car_actual in ABC: # Es letra, numero o punto?
                self.entrada.add(self.car_actual) #Los agregamos a self.entrada

                # Agregamos un parentesis izquierdo para tener el regex correcto
                yield Token(TokenType.PARI, '(') 
                yield Token(TokenType.LETRA, self.car_actual)

                self.Next()
                parentesis_cerrado = False # Se agregó parentesis de cierre?

                while (self.car_actual != None) and ( (self.car_actual in ABC) or (self.car_actual in '*+')):

                    # Creamos el token para el operador que estamos trabajando y agregamos el parentesis de cierre
                    if self.car_actual == '*':
                        yield Token(TokenType.KLEENE, '*')
                        yield Token(TokenType.PARD, ')')
                        parentesis_cerrado = True

                    elif self.car_actual == '+':
                        yield Token(TokenType.PLUS, '+')
                        yield Token(TokenType.PARD, ')')
                        parentesis_cerrado = True

                    elif self.car_actual in ABC:
                        self.entrada.add(self.car_actual)
                        yield Token(TokenType.UNION)
                        yield Token(TokenType.LETRA, self.car_actual)

                    self.Next()

                    # Si el ctual es un "(" y se agregó un ")" al final, se genera un token de unión "."
                    if ((self.car_actual != None) and (self.car_actual == '(') and (parentesis_cerrado)):
                        yield Token(TokenType.UNION)


                # Si el ctual es un "(" y NO se agregó un ")" al final, se genera un token de PARD ")"  y de UNION "."
                if ((self.car_actual != None) and (self.car_actual == '(') and (not parentesis_cerrado)):
                    yield Token(TokenType.PARD, ')')
                    yield Token(TokenType.UNION)

                elif not parentesis_cerrado:
                    yield Token(TokenType.PARD, ')')

            # Se crea y agrega el caracter dependiendo si es | ( ) * +

            elif self.car_actual == '|':
                self.Next()
                yield Token(TokenType.OR, '|')

            elif self.car_actual == '(':
                self.Next()
                yield Token(TokenType.PARI)

            elif self.car_actual in (')*+'):

                if self.car_actual == ')':
                    self.Next()
                    yield Token(TokenType.PARD)

                elif self.car_actual == '*':
                    self.Next()
                    yield Token(TokenType.KLEENE)

                elif self.car_actual == '+':
                    self.Next()
                    yield Token(TokenType.PLUS)

                # verifica si aun existe algun token agrega una union
                if ((self.car_actual != None) and ((self.car_actual in ABC) or (self.car_actual == '('))):
                    yield Token(TokenType.UNION, '.')

            else:
                raise Exception(f'Caracter no valido: {self.car_actual}')

    #devolvemos todos los simbolos que esten en self.entrada
    def obtenerSimbolos(self):
        return self.entrada