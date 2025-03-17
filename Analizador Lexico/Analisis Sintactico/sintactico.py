import ply.yacc as yacc
from lexer import tokens, lexer_sintactico

# --------------------------
# Clases para el AST
# --------------------------

class Node:
    pass

class Expression(Node):
    pass

class Statement(Node):
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

#Clases para las sentencias
class Block(Statement):
    def __init__(self, statements):
        self.statements = statements

class VariableDeclaration(Statement):
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value

class Assignment(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IfStatement(Statement):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition  # Expresión booleana
        self.then_block = then_block  # Block
        self.else_block = else_block  # Block u otro IfStatement (para else if)

class ForStatement(Statement):
    def __init__(self, type, iterator, iterable, block):
        self.type = type
        self.iterator = iterator
        self.iterable = iterable
        self.block = block

class WhileStatement(Statement):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value

class FunctionDeclaration(Statement):
    def __init__(self, modificador_acceso, static, tipo_retorno, nombre, parametros, cuerpo):
        self.modificador_acceso = modificador_acceso  
        self.static = static  
        self.tipo_retorno = tipo_retorno  
        self.nombre = nombre  
        self.parametros = parametros  
        self.cuerpo = cuerpo  

# Clases para las expresiones

class Print(Expression):
    def __init__(self, value):
        self.value = value

class BinOp(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(Expression):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Increment(Statement):
    def __init__(self, identifier, is_pre=True):
        self.identifier = identifier
        self.is_pre = is_pre

class Decrement(Statement):
    def __init__(self, identifier, is_pre=True):
        self.identifier = identifier
        self.is_pre = is_pre

class Literal(Expression):
    def __init__(self, value, type):
        self.value = value
        self.type = type  # 'num', 'dec', 'bool', 'str'

class Identifier(Expression):
    def __init__(self, name):
        self.name = name

# --------------------------
# Reglas del parser
# --------------------------

errores_sintacticos = ""

precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVISION', 'MODULO'),
    ('right', 'UMENOS'),
)


# Reglas para el programa

def p_empty(p):
    'empty :'
    pass

def p_program(p):
    '''program : lineas'''
    p[0] = Program(p[1])

def p_lineas(p):
    '''lineas : lineas line
              | line'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_line(p):
    '''line : expresion PUNTOYCOMA
            | sentencia'''
    p[0] = p[1]


# Reglas para sentencias

def p_sentencia(p):
    '''sentencia : declaracion
                | sentencia_if
                | sentencia_for
                | sentencia_while
                | sentencia_funcion_declaracion
                | return'''  # Sentencia vacía (;)
    p[0] = p[1]

def p_sentencia_block(p):
    'sentencia_block : ILLAVE statements DLLAVE'
    p[0] = Block(p[2])  # Block es una clase del AST para agrupar sentencias

def p_statements(p):
    '''statements : statements line
                  | line'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaracion(p):
    'declaracion : TIPO_DATO IDENTIFICADOR IGUAL expresion PUNTOYCOMA'
    p[0] = VariableDeclaration(p[1], Identifier(p[2]), p[4])

def p_asignacion(p):
    'sentencia : IDENTIFICADOR IGUAL expresion PUNTOYCOMA'
    p[0] = Assignment(Identifier(p[1]), p[3])

def p_sentencia_if(p):
    '''sentencia_if : IF IPARENTESIS expresion DPARENTESIS sentencia_block ELSE sentencia_if
                    | IF IPARENTESIS expresion DPARENTESIS sentencia_block
                    | IF IPARENTESIS expresion DPARENTESIS sentencia_block ELSE sentencia_block'''
    if len(p) == 6:
        p[0] = IfStatement(p[3], p[5])  # if sin else
    else:
        # Permite que el else_block sea otro IfStatement (para else if)
        p[0] = IfStatement(p[3], p[5], p[7])

def p_sentencia_for(p):
    'sentencia_for : FOR IPARENTESIS TIPO_DATO IDENTIFICADOR DOSPUNTOS IDENTIFICADOR DPARENTESIS sentencia_block'
    p[0] = ForStatement(p[3], p[4], p[6], p[8])

def p_sentencia_while(p):
    'sentencia_while : WHILE IPARENTESIS expresion DPARENTESIS sentencia_block'
    p[0] = WhileStatement(p[3], p[5])

def p_modificador_acceso(p):
    '''modificador_acceso : MODIFICADOR_ACCESO
                            | empty'''
    p[0] = p[1]

def p_static(p):
    '''static : STATIC
                | empty'''
    p[0] = p[1]

def p_tipo_dato(p):
    '''tipo_dato : TIPO_DATO
                    | VOID'''
    p[0] = p[1]

def p_parametros(p):
    """parametros : parametros COMA TIPO_DATO IDENTIFICADOR 
                | TIPO_DATO IDENTIFICADOR
                | empty"""
    if len(p) == 4:
        p[0] = p[1] + [(p[2], p[3])]
    elif len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = []

def p_return(p):
    'return : RETURN expresion PUNTOYCOMA'
    p[0] = ReturnStatement(p[2])


def p_sentencia_funcion_declaracion(p):
    'sentencia_funcion_declaracion : modificador_acceso static tipo_dato IDENTIFICADOR IPARENTESIS parametros DPARENTESIS sentencia_block'
    p[0] = FunctionDeclaration(p[1], p[2], p[3], p[4], p[6], p[8])



# Reglas para expresiones

def p_expresion_print(p):
    'expresion : FUNCION_PRINTLN IPARENTESIS expresion DPARENTESIS'
    p[0] = Print(p[3])

def p_expresion_binaria_aritmetica(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVISION expresion
                 | expresion MODULO expresion'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expresion_binaria_logica(p):
    '''expresion : expresion AND expresion
                | expresion OR expresion
                | expresion MAYOR expresion
                | expresion MENOR expresion
                | expresion MAYOR_IGUAL expresion
                | expresion MENOR_IGUAL expresion
                | expresion IGUALDAD expresion
                | expresion DIFERENTE expresion'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expresion_unaria(p):
    'expresion : MENOS expresion %prec UMENOS'
    p[0] = UnaryOp('-', p[2])

def p_expresion_incremento_postfijo(p):
    'expresion : IDENTIFICADOR INCREMENTO'
    p[0] = Increment(Identifier(p[1]), is_pre=False)

def p_expresion_incremento_prefijo(p):
    'expresion : INCREMENTO IDENTIFICADOR'
    p[0] = Increment(Identifier(p[2]), is_pre=True)

def p_expresion_decremento_postfijo(p):
    'expresion : IDENTIFICADOR DECREMENTO'
    p[0] = Decrement(Identifier(p[1]), is_pre=False)

def p_expresion_decremento_prefijo(p):
    'expresion : DECREMENTO IDENTIFICADOR'
    p[0] = Decrement(Identifier(p[2]), is_pre=True)

def p_expresion_identificador(p):
    'expresion : IDENTIFICADOR'
    p[0] = Identifier(p[1])

def p_expresion_parentesis(p):
    'expresion : IPARENTESIS expresion DPARENTESIS'
    p[0] = p[2]

def p_expresion_numero(p):
    'expresion : NUMERO'
    p[0] = Literal(p[1], 'num')

def p_expresion_decimal(p):
    'expresion : DECIMAL'
    p[0] = Literal(p[1], 'dec')

def p_expresion_cadena(p):
    'expresion : CADENA'
    p[0] = Literal(p[1], 'str')

def p_expresion_booleano(p):
    'expresion : BOOLEANO'
    p[0] = Literal(p[1], 'bool')


def p_error(p):
    global errores_sintacticos
    if p:
        # Calcula la columna relativa a la línea actual
        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        column = (p.lexpos - line_start) + 1  # Ajusta para que comience en 1
        errores_sintacticos += f"Error de sintaxis en '{p.value}' (Línea {p.lineno}, Columna {column})\n"
    else:
        errores_sintacticos += "Error de sintaxis: estructura incompleta\n"

# --------------------------
# Construcción del parser
# --------------------------
parser = yacc.yacc(start='program')

# --------------------------
# Función de prueba
# --------------------------
def test_parser(data):
    global errores_sintacticos
    errores_sintacticos = ""
    lexer_sintactico.input(data)
    result = parser.parse(data, lexer=lexer_sintactico)
    
    if errores_sintacticos:
        return f"Errores:\n{errores_sintacticos}"
    else:
        return "Análisis sintáctico exitoso\nAST generado:\n" + ast_to_str(result)

def ast_to_str(node, indent=0, is_last=True, prefix=''):
    result = ""
    if isinstance(node, Program):
        result += ' ' * indent + prefix + "Programa\n"
        for i, stmt in enumerate(node.statements):
            result += ast_to_str(stmt, indent + 4, i == len(node.statements) - 1, "├── ")
    elif isinstance(node, BinOp):
        result += ' ' * indent + prefix + f"BinOp({node.op})\n"
        result += ast_to_str(node.left, indent + 4, False, "├── ")
        result += ast_to_str(node.right, indent + 4, True, "└── ")
    elif isinstance(node, UnaryOp):
        result += ' ' * indent + prefix + f"UnaryOp({node.op})\n"
        result += ast_to_str(node.expr, indent + 4, True, "└── ")
    elif isinstance(node, VariableDeclaration):
        result += ' ' * indent + prefix + f"Declaración: {node.var_type} {node.name.name}\n"
        result += ast_to_str(node.value, indent + 4, True, "└── ")
    elif isinstance(node, Assignment):
        result += ' ' * indent + prefix + f"Asignación: {node.name.name}\n"
        result += ast_to_str(node.value, indent + 4, True, "└── ")
    elif isinstance(node, Literal):
        result += ' ' * indent + prefix + f"Literal({node.type}): {node.value}\n"
    elif isinstance(node, Identifier):
        result += ' ' * indent + prefix + f"Identificador: {node.name}\n"
    elif isinstance(node, Increment):
        result += ' ' * indent + prefix + f"Incremento {'pre' if node.is_pre else 'post'}fijo: {node.identifier.name}\n"
    elif isinstance(node, Decrement):
        result += ' ' * indent + prefix + f"Decremento {'pre' if node.is_pre else 'post'}fijo: {node.identifier.name}\n"
    elif isinstance(node, Print):
        result += ' ' * indent + prefix + "Print\n"
        result += ast_to_str(node.value, indent + 4, True, "└── ")
    elif isinstance(node, IfStatement):
        result += ' ' * indent + prefix + "IfStatement\n"
        result += ' ' * (indent + 4) + "├── Condición\n"
        result += ast_to_str(node.condition, indent + 8, False, "│   └── ")
        result += ' ' * (indent + 4) + "├── Then\n"
        result += ast_to_str(node.then_block, indent + 8, node.else_block is None, "│   └── ")
        if node.else_block:
            result += ' ' * (indent + 4) + "└── Else\n"
            result += ast_to_str(node.else_block, indent + 8, True, "    └── ")
    elif isinstance(node, ForStatement):
        result += ' ' * indent + prefix + "ForStatement\n"
        result += ' ' * (indent + 4) + "├── ForArgument\n"
        result += ' ' * (indent + 8) + f"├── Iterador: {node.iterator}\n"
        result += ' ' * (indent + 8) + f"├── Tipo: {node.type}\n"
        result += ' ' * (indent + 8) + f"└── Iterable: {node.iterable}\n"
        result += ' ' * (indent + 4) + "└── ForBlock\n"
        result += ast_to_str(node.block, indent + 8, True, "    └── ")
    elif isinstance(node, WhileStatement):
        result += ' ' * indent + prefix + "WhileStatement\n"
        result += ' ' * (indent + 4) + "├── Condición\n"
        result += ast_to_str(node.condition, indent + 8, False, "│   └── ")
        result += ' ' * (indent + 4) + "└── Then\n"
        result += ast_to_str(node.block, indent + 8, True, "    └── ")
    elif isinstance(node, ReturnStatement):
        result += ' ' * indent + prefix + "ReturnStatement\n"
        result += ast_to_str(node.value, indent + 4, True, "└── ")
    elif isinstance(node, FunctionDeclaration):
        result += ' ' * indent + prefix + "FunctionDeclaration\n"
        result += ' ' * (indent + 4) + f"├── Modificador: {node.modificador_acceso or 'Ninguno'}\n"
        result += ' ' * (indent + 4) + f"├── Static: {'Sí' if node.static else 'No'}\n"
        result += ' ' * (indent + 4) + f"├── Tipo Retorno: {node.tipo_retorno}\n"
        result += ' ' * (indent + 4) + f"├── Nombre: {node.nombre}\n"
        result += ' ' * (indent + 4) + "├── Parámetros\n"
        for tipo, nombre in node.parametros:
            result += ' ' * (indent + 8) + f"├── {tipo} {nombre}\n"
        result += ' ' * (indent + 4) + "└── Cuerpo\n"
        result += ast_to_str(node.cuerpo, indent + 8, True, "    └── ")
    elif isinstance(node, Block):
        result += ' ' * indent + prefix + "Block\n"
        for i, stmt in enumerate(node.statements):
            result += ast_to_str(stmt, indent + 4, i == len(node.statements) - 1, "└── ")
    return result

# Prueba
data = """
int x = 3;
int y = 1;

if (x > y) {
    int z = x + y;
    5-3;
} else if (z > y) {
    5 - (3*2.5);
}

int w = 2;
for (int numero : numeros) {
    if (numero > 0) {
        System.out.println("El numero: " + numero + " es positivo");
    }
}

while (i < 11) {
           sum = sum + i;
           i++;
           if (5+3 == 8) {
            System.out.println("El numero: " + numero + " es positivo");
        }
       }
public static int fibonacci(int n) {
        if (n == 0) {
            return 0; 
        } else if (n == 1) {
            return 1;
        } else {
            return numero;
        }
    }
"""
print(test_parser(data))
