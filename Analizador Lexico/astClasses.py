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
    def __init__(self, access_modifier , static ,var_type, name, value):
        self.access_modifier = access_modifier  
        self.static = static
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

class FunctionDeclarationMain(Statement):
    def __init__(self, declaracion, cuerpo):
        self.declaracion = declaracion
        self.cuerpo = cuerpo
class ClassDeclaration(Statement):
    def __init__(self, access_modifier, name, body):
        self.access_modifier = access_modifier
        self.name = name
        self.body = body

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

class FunctionCall(Expression):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments