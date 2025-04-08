from astClasses import *

#Metodos de ayuda


class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
        self.current_scope = 0
        self.params_functions = {}

    def enter_scope(self, origin):
        print(f"Entrando al scope {self.current_scope + 1}")
        self.scopes.append({ origin: { "type": "Origen", "kind": "Scope" } })
        self.current_scope += 1

    def exit_scope(self):
        """ self.scopes.pop() """
        self.current_scope -= 1

    def add_symbol(self, name, symbol_type, kind, params=None, origin=None):
        self.scopes[self.current_scope][name] = {'type': symbol_type, 'kind': kind}
        if kind == 'funcion':
            self.scopes[self.current_scope][name]['params'] = params
        if origin:
            self.scopes[self.current_scope][name]['origin'] = origin

    def lookup(self, name):
        if name in self.scopes[self.current_scope]:
            return self.scopes[self.current_scope][name]
        """ for scope in reversed(self.scopes):
            print("Buscando", name, "en", scope)
            if name in scope:
                return scope[name] """
        return None
    def get_symbols_as_string(self):
        output = ""
        print("All scopes",self.scopes)
        for i, scope in enumerate(self.scopes):
            output += f"Scope {i}:\n"
            for name, details in scope.items():
                output += f"  - {name}: tipo={details['type']}, clase={details['kind']}"
                if 'params' in details:
                    output += f", parámetros={details['params']}"
                output += "\n"

        return output

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function = None

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for _, value in vars(node).items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, Node):
                        self.visit(item)
            elif isinstance(value, Node):
                self.visit(value)
    

    def get_expr_type(self, expr):

        

        # Si es un literal, retorna su tipo (int, float, etc.)
        if isinstance(expr, Literal):
            return expr.type
    
        # Si es un identificador, busca su tipo en la tabla de símbolos
        elif isinstance(expr, Identifier):
            symbol = self.symbol_table.lookup(expr.name)
            if not symbol:
                self.errors.append(f"Identificador no declarado: \"{expr.name}\"")
                return None
            return symbol['type']
    
        # Si es una operación binaria (ej: a + b)
        elif isinstance(expr, BinOp):
            #Si es un booleano si el operador es de tipo booleano
            if expr.op == "==" or expr.op == "!=" or expr.op == ">" or expr.op == "<" or expr.op == ">=" or expr.op == "<=" or expr.op == "&&" or expr.op == "||":
                return "boolean"
            left_type = self.get_expr_type(expr.left)
            right_type = self.get_expr_type(expr.right)
        
            # Validar compatibilidad de tipos
            if left_type != right_type:
                self.errors.append(f"Tipos incompatibles en operación \"{expr.op}\": {left_type} y {right_type}")
                return None
        
            if expr.op in ("/", "%"):
                # Verificar si el lado derecho es un literal cero
                if isinstance(expr.right, Literal):
                    if expr.right.value == 0 or expr.right.value == 0.0:
                        self.errors.append(f"División por cero detectada en operación \"{expr.op}\"")
        
            # Determinar el tipo resultante (ej: int + int -> int)
            return left_type  # Asume que el tipo resultante es el mismo que los operandos
    
        # Si es una llamada a función, retorna el tipo de retorno
        elif isinstance(expr, FunctionCall):
            func_info = self.symbol_table.lookup(expr.name)
            if not func_info:
                return None
            return func_info['type']
    
        # Otros casos (ajusta según tu AST)
        else:
            return None

    def get_symbol_table(self):
        return self.symbol_table.get_symbols_as_string()
    # ------------------------------
    # Métodos para cada nodo del AST
    # ------------------------------
    
    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VariableDeclaration(self, node):
        # Verificar si la variable ya existe en el mismo scope
        existing = self.symbol_table.lookup(node.name.name)
        if existing:
            self.errors.append(f"Variable \"{node.name.name}\" ya está declarada o identificador \"{node.name.name}\" ya usado ")
        else:
            # Registrar en la tabla de símbolos
            self.symbol_table.add_symbol(node.name.name, node.var_type, 'variable')
        # Validar tipo de la expresión asignada (si existe)
        if node.value:
            # Obtener el tipo de la expresión (maneja BinOp, Literal, etc.)
            expr_type = self.get_expr_type(node.value)
        
            if expr_type and expr_type != node.var_type:
                self.errors.append(f"Tipo incompatible en asignación: {node.var_type} vs {expr_type}")

    def visit_FunctionDeclaration(self, node):
        # Registrar función en el scope global
        existing = self.symbol_table.lookup(node.nombre)
        if existing:
            self.errors.append(f"Función \"{node.nombre}\" ya declarada o identificador \"{node.nombre}\" ya usado ")
        else:    
            self.symbol_table.add_symbol(node.nombre, node.tipo_retorno, 'funcion', len(node.parametros))
        # Entrar a nuevo scope (parámetros y variables locales)
        self.symbol_table.enter_scope(origin = node.nombre)
        # Registrar parámetros
        lista_parametros = []
        for param in node.parametros:
            self.symbol_table.add_symbol(param[1], param[0], 'variable', origin = node.nombre)
            lista_parametros.append({'name': param[1], 'type': param[0]})
        
        self.symbol_table.params_functions[node.nombre+str(self.symbol_table.current_scope)] = lista_parametros
        # Validar cuerpo
        self.visit(node.cuerpo)
        self.symbol_table.exit_scope()

    def visit_FunctionCall(self, node):
        func_info = None
        for scope in self.symbol_table.scopes:
            if node.name in scope:
                func_info = scope[node.name]
                break
        if not func_info:
            self.errors.append(f"Función \"{node.name}\" no declarada")
            return
    
    # Verificar número de argumentos
        if len(node.arguments) != func_info['params']:
            self.errors.append(f"Número incorrecto de argumentos en {node.name}")
    
    # Verificar tipos de argumentos
        if len(node.arguments) == func_info['params']:
            for i in range(len(node.arguments)):
                arg_type = self.get_expr_type(node.arguments[i])
                param_type = self.symbol_table.params_functions[ node.name+str(self.symbol_table.current_scope)][i]['type']
                if arg_type != param_type:
                    self.errors.append(f"Tipo de argumento incorrecto en {node.name}: se esperaba {param_type}, se recibió {arg_type}")
    # ... Agregar métodos para otros nodos (IfStatement, ForStatement, etc.) ...

    def visit_Literal(self, node):
        # Retornar el tipo del literal
        return node.type