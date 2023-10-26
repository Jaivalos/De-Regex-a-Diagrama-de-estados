# Libreria para numeración
from enum import Enum

# Numeración para tipos de tokens
class TokenType(Enum):
    LETRA = 0 
    UNION = 1   
    OR = 2
    KLEENE = 3  
    PLUS = 4
    PARD = 5    
    PARI = 6    

# Clase para representar un token
class Token:
    def __init__(self, type: TokenType, value=None):
        self.type = type        # Tipo de token
        self.value = value      # Valor asociado al token (opcional)
        self.precedence = type.value  # Precedencia basada en el valor del tipo

    def __repr__(self):
        return f'{self.type.name}: {self.value}'  # Representación de cadena del token
