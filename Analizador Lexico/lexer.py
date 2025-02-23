import ply.lex as lex

#Variable que captura los mensajes de error
errores = ""
mensaje = ""

# Definición de tokens
tokens = [
    'MAS', 'MENOS', 'POR', 'DIVISION', 'NUMERO', 'IDENTIFICADOR', 'IGUAL', 
    'PALABRA_RESERVADA', 'IPARENTESIS', 'DPARENTESIS', 'ICORCHETE', 'DCORCHETE', 
    'ILLAVE', 'DLLAVE', 'MENOR', 'MAYOR', 'IGUALDAD', 'DIFERENTE', 'MENOR_IGUAL', 'MAYOR_IGUAL',
    'MAS_IGUAL', 'MENOS_IGUAL', 'POR_IGUAL', 'DIVISION_IGUAL', 'MODULO', 'MODULO_IGUAL', 'AND', 'OR', 'PUNTOYCOMA', 'COMENTARIO',
    'CADENA', 'PUNTO', 'INCREMENTO', 'DECREMENTO'
]

# Expresiones regulares para tokens simples
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVISION = r'\/'
t_MENOR = r'\<'
t_MAYOR = r'\>'
t_IGUAL = r'\='
t_IGUALDAD = r'=='
t_DIFERENTE = r'!='
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_MAS_IGUAL = r'\+='
t_MENOS_IGUAL = r'-='
t_POR_IGUAL = r'\*='
t_DIVISION_IGUAL = r'/='
t_MODULO = r'%'
t_MODULO_IGUAL = r'%='
t_AND = r'\&&'
t_OR = r'\|\|'
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'\-\-'




t_IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_IPARENTESIS = r'\('
t_DPARENTESIS = r'\)'
t_ICORCHETE = r'\['
t_DCORCHETE = r'\]'
t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_CADENA = r'\"[^\"]*\"'
t_PUNTOYCOMA = r';'
t_PUNTO = r'\.'

# Palabras reservadas
t_PALABRA_RESERVADA = r'if|else|while|switch|case|default|break|continue|do|for|return|try|catch|finally|throw|throws|' \
    r'public|private|protected|static|final|abstract|synchronized|volatile|class|void|args|' \
    r'int|long|float|double|char|boolean|String|' \
    r'null|true|false'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Token para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMENTARIO(t):
    r'\/\/.*'
    t.value = t.value[2:]
    return t

# Manejo de errores léxicos
def t_error(t):
    global errores
    errores += f"Expresion Invalida \"{t.value}\" en la posicion: ({t.lineno},{t.lexpos})" + "\n"
    t.lexer.skip(1)

# Manejo de saltos de linea para actualizar el contador de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



# Función para probar el analizador
def test_lexer(data):
    # Construir el analizador léxico
    lexer = lex.lex()
    lexer.input(data)
    global mensaje
    global errores
    mensaje = ""
    errores = ""

    mensaje += f"{'Tipo de Token':<27} {'Valores':<15} {'  Posiciones':>5}\n"

    while True:
        tok = lexer.token()
        if not tok:
            break

        mensaje += f"Token: {tok.type:<20} Valor: {tok.value:<10} Posición: ({tok.lineno:>2}, {tok.lexpos:>3})\n"

    if errores:
        mensaje += f"\nExpresiones Invalidas:\n{errores}" 
    else:
        mensaje += "\nNo se Encontraron Expresiones Invalidas."
    return mensaje

