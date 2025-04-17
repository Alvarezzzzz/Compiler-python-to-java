import ply.yacc as yacc
from lexer import tokens, lexer_sintactico
from semantic import SemanticAnalyzer  # <-- Agregar esta línea
from astClasses import *  # <-- Asegúrate de que las clases del AST estén definidas aquí

# --------------------------
# Clases para el AST
# --------------------------

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
                | sentencia_clase_declaracion
                | sentencia_funcion_declaracion_main
                | return'''  # Sentencia vacía (;)
    p[0] = p[1]

def p_sentencia_block(p):
    'sentencia_block : ILLAVE statements DLLAVE'
    p[0] = Block(p[2])  # Block es una clase del AST para agrupar sentencias

def p_sentencia_block_class(p):
    'sentencia_block_class : ILLAVE statements DLLAVE'
    p[0] = Block(p[2])  # Block es una clase del AST para agrupar sentencias

def p_statements(p):
    '''statements : statements line
                  | line'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


""" def p_line_or_empty(p):
    '''line_or_empty : line line_or_empty
                    | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_statements_class(p):
    'statements_class : line_or_empty sentencia_funcion_declaracion_main line_or_empty'
    p[0] = p[1] + [p[2]] + p[3] """


def p_declaracion(p):
    '''declaracion : modificador_acceso static tipo_dato IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                    | modificador_acceso static tipo_dato IDENTIFICADOR PUNTOYCOMA'''
    if len(p) == 8:
        p[0] = VariableDeclaration(p[1], p[2], p[3], Identifier(p[4]), p[6])
    else:
        # Declaración sin inicialización
        # Se crea una VariableDeclaration sin valor
        # Se asume que el valor es None o vacío
        # Esto puede ser ajustado según la lógica del lenguaje
        p[0] = VariableDeclaration(p[1], p[2], p[3], Identifier(p[4]), None)

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
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
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

def p_sentencia_funcion_declaracion_main(p):
    'sentencia_funcion_declaracion_main : FUNCION_MAIN sentencia_block'
    p[0] = FunctionDeclarationMain(p[1], p[2])

def p_sentencia_clase_declaracion(p):
    'sentencia_clase_declaracion : modificador_acceso CLASS IDENTIFICADOR sentencia_block_class'
    p[0] = ClassDeclaration(p[1], p[3], p[4])

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
    p[0] = Literal(p[1], 'int')

def p_expresion_decimal(p):
    'expresion : DECIMAL'
    p[0] = Literal(p[1], 'double')

def p_expresion_cadena(p):
    'expresion : CADENA'
    p[0] = Literal(p[1], 'String')

def p_expresion_booleano(p):
    'expresion : BOOLEANO'
    p[0] = Literal(p[1], 'boolean')

def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                | expresion
                | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_llamada_funcion(p):
    'expresion : IDENTIFICADOR IPARENTESIS argumentos DPARENTESIS'
    p[0] = FunctionCall(p[1], p[3])

def p_error(p):
    global errores_sintacticos
    if p:
        # Calcula la columna relativa a la línea actual
        line_start = p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        column = (p.lexpos - line_start) + 1  # Ajusta para que comience en 1
        errores_sintacticos += f"Error de sintaxis en \"{p.value}\" (Linea {p.lineno}, Columna {column})\n"
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
    data2 = data.replace("public static void main(String[] args)", "FUNCION_MAIN_ESPECIAL")  # Reemplazar la palabra "public static void main(String[] args)"
    lexer_sintactico.input(data2)
    result = parser.parse(data2, lexer=lexer_sintactico)
    
    if errores_sintacticos:
        return f"Errores:\n{errores_sintacticos}"
    else:
        # Realiza el análisis semántico
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(result) # Recorre el AST 
        
        mensaje = ""
        if semantic_analyzer.errors:
            # Si hay errores semánticos, los concatenamos en un mensaje
            mensaje += "Errores semanticos:\n"
            for error in semantic_analyzer.errors:
                mensaje += f"{error}\n"
        else:
            mensaje += "Análisis semántico exitoso\n"
            from translator import translate_to_python
            python_code = translate_to_python(result)
            print(f"Codigo traducido a Python:\n{python_code}")

        return "Análisis sintáctico exitoso\nAST generado:\n" + ast_to_str(result) + mensaje + "\n" + semantic_analyzer.get_symbol_table()

def ast_to_str(node, indent=0):
    result = ""
    
    def line(text, level):
        return " " * level + "└── " + text + "\n"
    
    if isinstance(node, Program):
        # Regla: program : lineas
        result += line("<program>", indent)
        for stmt in node.statements:
            result += ast_to_str(stmt, indent + 4)
        return result

    elif isinstance(node, VariableDeclaration):
        # Regla: declaracion : TIPO_DATO IDENTIFICADOR IGUAL expresion PUNTOYCOMA
        result += line("<declaracion>", indent)
        if node.access_modifier:
            result += line(node.access_modifier, indent + 4)          # MODIFICADOR_ACCESO (terminal)
        if node.static:
            result += line("static", indent + 4)                     # Terminal "static"
        result += line(str(node.var_type), indent + 4)           # TIPO_DATO (terminal)
        result += line(node.name.name, indent + 4)                # IDENTIFICADOR (terminal)
        result += line("=", indent + 4)                           # Terminal "="
        result += line("<expresion>", indent + 4)                 # Nodo no terminal: expresion
        result += ast_to_str(node.value, indent + 8)
        result += line(";", indent + 4)                           # Terminal ";" 
        return result

    elif isinstance(node, Assignment):
        # Regla: sentencia : IDENTIFICADOR IGUAL expresion PUNTOYCOMA
        result += line("<asignacion>", indent)
        result += line(node.name.name, indent + 4)                # IDENTIFICADOR
        result += line("=", indent + 4)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.value, indent + 8)
        result += line(";", indent + 4)
        return result

    elif isinstance(node, IfStatement):
        # Regla aproximada: sentencia_if : IF IPARENTESIS expresion DPARENTESIS sentencia_block [ELSE sentencia_block]
        result += line("<sentencia_if>", indent)
        result += line("IF", indent + 4)
        result += line("(", indent + 4)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.condition, indent + 8)
        result += line(")", indent + 4)
        # Imprime directamente el nodo Block en lugar de "<sentencia_block>"
        result += ast_to_str(node.then_block, indent + 4)
        if node.else_block:
            result += line("ELSE", indent + 4)
            result += ast_to_str(node.else_block, indent + 4)
        return result

    elif isinstance(node, ForStatement):
        # Regla: sentencia_for : FOR IPARENTESIS TIPO_DATO IDENTIFICADOR DOSPUNTOS IDENTIFICADOR DPARENTESIS sentencia_block
        result += line("<sentencia_for>", indent)
        result += line("FOR", indent + 4)
        result += line("(", indent + 4)
        result += line(node.type, indent + 4)                   # TIPO_DATO
        result += line(node.iterator, indent + 4)               # IDENTIFICADOR
        result += line(":", indent + 4)
        result += line(node.iterable, indent + 4)               # IDENTIFICADOR (iterable)
        result += line(")", indent + 4)
        # Imprime directamente el bloque
        result += ast_to_str(node.block, indent + 4)
        return result

    elif isinstance(node, WhileStatement):
        # Regla: sentencia_while : WHILE IPARENTESIS expresion DPARENTESIS sentencia_block
        result += line("<sentencia_while>", indent)
        result += line("WHILE", indent + 4)
        result += line("(", indent + 4)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.condition, indent + 8)
        result += line(")", indent + 4)
        # Imprime directamente el bloque
        result += ast_to_str(node.block, indent + 4)
        return result

    elif isinstance(node, ReturnStatement):
        # Regla: return : RETURN expresion PUNTOYCOMA
        result += line("<return>", indent)
        result += line("return", indent + 4)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.value, indent + 8)
        result += line(";", indent + 4)
        return result

    elif isinstance(node, FunctionDeclaration):
        # Regla: sentencia_funcion_declaracion : modificador_acceso static tipo_dato IDENTIFICADOR IPARENTESIS parametros DPARENTESIS sentencia_block
        result += line("<sentencia_funcion_declaracion>", indent)
        if node.modificador_acceso:
            result += line(node.modificador_acceso, indent + 4)
        if node.static:
            result += line("static", indent + 4)
        result += line(node.tipo_retorno, indent + 4)
        result += line(node.nombre, indent + 4)
        result += line("(", indent + 4)
        result += line("<parametros>", indent + 4)
        for tipo, ident in node.parametros:
            result += line(tipo + " " + ident, indent + 8)
        result += line(")", indent + 4)
        # Imprime directamente el bloque de la función
        result += ast_to_str(node.cuerpo, indent + 4)
        return result

    elif isinstance(node, FunctionDeclarationMain):
        # Regla: sentencia_funcion_declaracion_main : FUNCION_MAIN sentencia_block
        result += line("<sentencia_funcion_declaracion_main>", indent)
        #public static void main(String[] args) 
        result += line("public", indent + 4)
        result += line("static", indent + 4)
        result += line("void", indent + 4)
        result += line("main", indent + 4)
        result += line("(", indent + 4)
        result += line("String[]", indent + 4)
        result += line("args", indent + 4)
        result += line(")", indent + 4)
        # Imprime directamente el bloque de la función
        result += ast_to_str(node.cuerpo, indent + 4)
        return result

    elif isinstance(node, ClassDeclaration):
        # Regla: sentencia_clase_declaracion : modificador_acceso CLASS IDENTIFICADOR sentencia_block
        result += line("<sentencia_clase_declaracion>", indent)
        if node.access_modifier:
            result += line(node.access_modifier, indent + 4)
        result += line("class", indent + 4)
        result += line(node.name, indent + 4)
        # Imprime directamente el bloque de la clase
        result += ast_to_str(node.body, indent + 4)
        return result

    elif isinstance(node, Print):
        # Regla: expresion : FUNCION_PRINTLN IPARENTESIS expresion DPARENTESIS
        result += line("<print>", indent)
        result += line("System.out.println", indent + 4)
        result += line("(", indent + 4)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.value, indent + 8)
        result += line(")", indent + 4)
        return result

    elif isinstance(node, BinOp):
        # Regla: expresion : expresion OP expresion
        result += line("<BinOp>", indent)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.left, indent + 8)
        result += line(node.op, indent + 4)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.right, indent + 8)
        return result

    elif isinstance(node, UnaryOp):
        # Regla: expresion : MENOS expresion %prec UMENOS
        result += line("<unaria>", indent)
        result += line(node.op, indent + 4)
        result += line("<expresion>", indent + 4)
        result += ast_to_str(node.expr, indent + 8)
        return result

    elif isinstance(node, Increment):
        # Incremento prefijo o postfijo
        if node.is_pre:
            result += line("<incremento_prefijo>", indent)
            result += line("INCREMENTO", indent + 4)
            result += line(node.identifier.name, indent + 4)
        else:
            result += line("<incremento_postfijo>", indent)
            result += line(node.identifier.name, indent + 4)
            result += line("INCREMENTO", indent + 4)
        return result

    elif isinstance(node, Decrement):
        # Decremento prefijo o postfijo
        if node.is_pre:
            result += line("<decremento_prefijo>", indent)
            result += line("DECREMENTO", indent + 4)
            result += line(node.identifier.name, indent + 4)
        else:
            result += line("<decremento_postfijo>", indent)
            result += line(node.identifier.name, indent + 4)
            result += line("DECREMENTO", indent + 4)
        return result

    elif isinstance(node, FunctionCall):
        # Regla: expresion : IDENTIFICADOR IPARENTESIS argumentos DPARENTESIS
        result += line("<function_call>", indent)
        result += line(node.name, indent + 4)
        result += line("(", indent + 4)
        result += line("<argumentos>", indent + 4)
        for arg in node.arguments:
            result += ast_to_str(arg, indent + 8)
        result += line(")", indent + 4)
        return result

    elif isinstance(node, Block):
        # Regla: sentencia_block : ILLAVE statements DLLAVE
        result += line("<block>", indent)
        for stmt in node.statements:
            result += ast_to_str(stmt, indent + 4)
        return result

    elif isinstance(node, Literal):
        # Nodo terminal: Literal
        result += line(str(node.value), indent)
        return result

    elif isinstance(node, Identifier):
        # Nodo terminal: Identificador
        result += line(node.name, indent)
        return result

    else:
        return result





