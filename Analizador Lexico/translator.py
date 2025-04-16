from astClasses import *

class PythonCodeGenerator:
    def __init__(self):
        self.output = []
        self.indent_level = 0
        self.current_class = None
    
    @property
    def indent(self):
        return ' ' * 4 * self.indent_level

    def generate(self, node):
        self.visit(node)
        return '\n'.join(self.output)

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        print("METHOD NAME", method_name)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        pass

    def visit_Program(self, node):
        for stmt in node.statements:
            print("Visitando nodo DESDE EL TRANSLATOR:", stmt)
            self.visit(stmt)

    def visit_VariableDeclaration(self, node):
        if node.value:
            value_code = self._get_expression_code(node.value)
            self.output.append(f"{self.indent}{node.name.name} = {value_code}")

    def visit_FunctionDeclaration(self, node):
        params = ', '.join([p[1] for p in node.parametros])
        
        # Solo agregar decorador @staticmethod si está dentro de una clase
        decorator = '@staticmethod\n' if node.static and self.current_class else ''
        
        self.output.append(f"{self.indent}{decorator}{self.indent}def {node.nombre}({params}):")
        self.indent_level += 1
        self.visit(node.cuerpo)
        self.indent_level -= 1
        self.output.append('')
    
    def visit_ReturnStatement(self, node):
        print("Visitando nodo RETURN:", node)
        if node.value:
            value_code = self._get_expression_code(node.value)
            self.output.append(f"{self.indent}return {value_code}")
        else:
            self.output.append(f"{self.indent}return")

    def visit_FunctionDeclarationMain(self, node):
        self.output.append("\nif __name__ == \"__main__\":")
        self.indent_level += 1
        self.visit(node.cuerpo)
        self.indent_level -= 1

    def visit_ClassDeclaration(self, node):
        if node.name == "Main" and self._has_main_method(node):
            self.visit_main_class(node)
        else:
            self.current_class = node.name
            self.output.append(f"\nclass {node.name}:")
            self.indent_level += 1
            self.visit(node.body)
            self.indent_level -= 1
            self.current_class = None

    def _has_main_method(self, class_node):
        for stmt in class_node.body.statements:
            if isinstance(stmt, FunctionDeclarationMain):
                return True
        return False

    def visit_main_class(self, node):
        # Procesar todos los elementos de la clase Main
        for stmt in node.body.statements:
            if isinstance(stmt, FunctionDeclarationMain):
                self.visit(stmt)
            else:
                # Traducir otros métodos como funciones globales
                self.visit(stmt)

    def visit_IfStatement(self, node):
        condition = self._get_expression_code(node.condition)
        self.output.append(f"{self.indent}if {condition}:")
        self.indent_level += 1
        self.visit(node.then_block)
        self.indent_level -= 1
        
        if node.else_block:
            self.output.append(f"{self.indent}else:")
            self.indent_level += 1
            self.visit(node.else_block)
            self.indent_level -= 1

    def visit_ForStatement(self, node):
        iterator = node.iterator
        iterable = node.iterable
        self.output.append(f"{self.indent}for {iterator} in {iterable}:")
        self.indent_level += 1
        self.visit(node.block)
        self.indent_level -= 1

    def visit_WhileStatement(self, node):
        condition = self._get_expression_code(node.condition)
        self.output.append(f"{self.indent}while {condition}:")
        self.indent_level += 1
        self.visit(node.block)
        self.indent_level -= 1

    def visit_Print(self, node):
        value = self._get_expression_code(node.value)
        self.output.append(f"{self.indent}print({value})")

    def visit_BinOp(self, node):
        left = self._get_expression_code(node.left)
        right = self._get_expression_code(node.right)
        op = self._translate_operator(node.op)
        return f"{left} {op} {right}"

    def visit_Identifier(self, node):
        return node.name

    def visit_Literal(self, node):
        if node.type == 'String':
            return f'{node.value}'
        return str(node.value)

    def _get_expression_code(self, expr):
        if isinstance(expr, (Identifier, Literal)):
            return self.visit(expr)
        elif isinstance(expr, BinOp):
            return self.visit_BinOp(expr)
        elif isinstance(expr, FunctionCall):
            return self.get_expresion_call_function(expr)
        return ''

    def get_expresion_call_function(self, node):
        args = ', '.join([self._get_expression_code(arg) for arg in node.arguments])
        return f"{node.name}({args})"   
    def _translate_operator(self, op):
        translations = {
            '&&': 'and',
            '||': 'or',
            '!=': '!=',
            '==': '==',
            '++': '+= 1',
            '--': '-= 1'
        }
        return translations.get(op, op)

    def visit_FunctionCall(self, node):
        args = ', '.join([self._get_expression_code(arg) for arg in node.arguments])
        self.output.append(f"{self.indent}{node.name}({args})")

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

def translate_to_python(ast):
    generator = PythonCodeGenerator()
    return generator.generate(ast)