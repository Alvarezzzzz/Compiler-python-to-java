import ply.lex as lex

# Variable que captura los mensajes de error
errores = ""
mensaje = ""

# Palabras reservadas
reservadas = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'switch': 'PALABRA_RESERVADA',
    'case': 'PALABRA_RESERVADA',
    'default': 'PALABRA_RESERVADA',
    'break': 'PALABRA_RESERVADA',
    'continue': 'PALABRA_RESERVADA',
    'do': 'PALABRA_RESERVADA',
    'for': 'FOR',
    'return': 'RETURN',
    'try': 'PALABRA_RESERVADA',
    'catch': 'PALABRA_RESERVADA',
    'finally': 'PALABRA_RESERVADA',
    'throw': 'PALABRA_RESERVADA',
    'throws': 'PALABRA_RESERVADA',
    'public': 'MODIFICADOR_ACCESO',
    'private': 'MODIFICADOR_ACCESO',
    'protected': 'MODIFICADOR_ACCESO',
    'static': 'STATIC',
    'final': 'PALABRA_RESERVADA',
    'abstract': 'PALABRA_RESERVADA',
    'synchronized': 'PALABRA_RESERVADA',
    'volatile': 'PALABRA_RESERVADA',
    'class': 'CLASS',
    'void': 'VOID',
    'args': 'PALABRA_RESERVADA',
    'char': 'PALABRA_RESERVADA',
    'null': 'PALABRA_RESERVADA',
    'true': 'BOOLEANO',
    'false': 'BOOLEANO',
    'int': 'TIPO_DATO',
    'long': 'TIPO_DATO',
    'float': 'TIPO_DATO',
    'double': 'TIPO_DATO',
    'boolean': 'TIPO_DATO',
    'String': 'TIPO_DATO',
}


# Definición de tokens
tokens = [
    'FUNCION_MAIN' ,'FUNCION_PRINTLN', 'MAS', 'MENOS', 'POR', 'DIVISION', 'NUMERO', 'DECIMAL', 'IDENTIFICADOR', 'IGUALDAD', 'IGUAL',
    'IPARENTESIS', 'DPARENTESIS', 'ICORCHETE', 'DCORCHETE',
    'ILLAVE', 'DLLAVE', 'MENOR', 'MAYOR', 'DIFERENTE', 'MENOR_IGUAL', 'MAYOR_IGUAL',
    'MAS_IGUAL', 'MENOS_IGUAL', 'POR_IGUAL', 'DIVISION_IGUAL', 'MODULO', 'MODULO_IGUAL', 'AND', 'OR',
    'PUNTOYCOMA', 'COMENTARIO', 'CADENA', 'PUNTO', 'DOSPUNTOS' ,'INCREMENTO', 'DECREMENTO', 'COMA'
] + list(set(reservadas.values()))


def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_FUNCION_MAIN(t):
    r'FUNCION_MAIN_ESPECIAL'
    t.value = "public static void main(String[] args)"
    return t

def t_FUNCION_PRINTLN(t):
    r'System\.out\.println'
    return t

# Expresiones regulares para tokens simples
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVISION = r'\/'
t_MENOR = r'\<'
t_MAYOR = r'\>'
t_IGUALDAD = r'=='
t_IGUAL = r'\='
t_DIFERENTE = r'!='
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_MAS_IGUAL = r'\+='
t_MENOS_IGUAL = r'-='
t_POR_IGUAL = r'\*='
t_DIVISION_IGUAL = r'/='
t_MODULO = r'%'
t_MODULO_IGUAL = r'%='
t_AND = r'&&'
t_OR = r'\|\|'
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'\-\-'

t_IPARENTESIS = r'\('
t_DPARENTESIS = r'\)'
t_ICORCHETE = r'\['
t_DCORCHETE = r'\]'
t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_CADENA = r'\"[^\"]*\"'
t_PUNTOYCOMA = r';'
t_PUNTO = r'\.'
t_DOSPUNTOS = r'\:'
t_COMA = r'\,'
# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Token para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t



# Token para identificadores y palabras reservadas
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')  # Verifica si es palabra reservada o identificador
    return t

# Token para comentarios
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

# Construir el analizador léxico
lexer_sintactico = lex.lex()

# Función para probar el analizador
def test_lexer(data):
    lexer = lex.lex()
    data2 = data.replace("public static void main(String[] args)", "FUNCION_MAIN_ESPECIAL")  # Reemplazar la palabra "public static void main(String[] args)"
    
    print(data2)
    lexer.input(data2)
    
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

#Prueba del analizador


'''
print(test_lexer("""
5 == 3
"""))
'''
