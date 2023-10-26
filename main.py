
from textos import titulo, menu, despedida, carga
from reader import Reader
from parseo import Parser
from direct_reader import DirectReader
from direct_dfa import DDFA
import time


if __name__ == "__main__":
    print(titulo)
    opt = None
    regex = None
    method = None

    while opt != 0:
        print(menu)
        opt = input()

        if opt == '1':
            print("Ingresa la expresión regular: ")
            regex = input()

            try:
                reader = Reader(regex)
                tokens = reader.crearTokens()
                parser = Parser(tokens)
                tree = parser.Parse()

                direct_reader = DirectReader(regex)
                direct_tokens = direct_reader.CreateTokens()
                direct_parser = Parser(direct_tokens)
                direct_tree = direct_parser.Parse()

                print('\n\t¡Regex aceptada!')
                print('\tRegex corregida:', tree)

            except AttributeError as e:
                print(f'\n\tERR: Expresion invalida (Faltan parentesis)')

            except Exception as e:
                print(f'\n\tERR: {e}')

        if opt == '2':

            if not regex:
                print('\n\tERR: ¡Primero ingresa el REGEX!')
                opt = None

            else:
                
                print("Escribe una cadena para validar: ")
                regex_input = input('> ')
                ddfa = DDFA(direct_tree, direct_reader.GetSymbols(), regex_input)

                ddfa_regex = ddfa.EvalRegex()

                print('¿La cadena es valida en la expresión regular?')
                print('>', ddfa_regex)

                print("¿Deseas ver el diagrama de estados? (y - n)")
                generate_diagram = input()

                if generate_diagram == 'y':
                    print(carga)
                    time.sleep(3)
                    ddfa.GraphDFA()

                ddfa = None


        elif opt == '3':
            print(despedida)
            exit(1)