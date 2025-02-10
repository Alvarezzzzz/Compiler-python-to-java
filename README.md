# Trasnspiler-python-to-java

Lexer es un compilador de código fuente que traduce programas escritos en Python a código Java. Esto permite a los desarrolladores aprovechar la familiaridad y la flexibilidad de Python, al tiempo que se benefician del rendimiento y la portabilidad de Java.

### Objetivos
- Se centra en la compilación de código Python que sigue el paradigma de programación orientada a objetos.
- Soporta tipos de datos básicos, estructuras de control, funciones, clases y algunas características de programación orientada a objetos.
- El código Java generado utiliza clases y bibliotecas estándar de Java para garantizar la compatibilidad y el rendimiento.

### Arquitectura general:
- Análisis léxico: El código Python se divide en tokens (palabras clave, identificadores, operadores, etc.).
- Análisis sintáctico: Se construye un árbol de sintaxis abstracta (AST) que representa la estructura del programa Python.
- Análisis semántico: Se verifican errores de tipo y se asegura la coherencia del código.
- Generación de código intermedio: Se crea una representación intermedia del código, más fácil de optimizar y traducir.
- Optimización (opcional): Se aplican técnicas para mejorar el rendimiento del código Java generado.
- Generación de código Java: Se traduce el código intermedio a código Java, utilizando clases y bibliotecas estándar.


### Características
#### Lenguaje Python soportado:
- Tipos de datos: enteros, flotantes, cadenas, booleanos, listas diccionarios.
- Estructuras de control: if, elif, else, for, while.
- Funciones: definición, llamada, parámetros, retorno.
- Clases: definición, atributos, métodos, herencia simple.

#### Características de Java utilizadas:*
- Clases y objetos.
- Tipos de datos primitivos y objetos.
- Estructuras de control: if, else, for, while.
- Métodos y constructores.
- Herencia e interfaces.

### Limitaciones:
- No se soportan características avanzadas de Python como generadores, decoradores o gestión de excepciones compleja.
- La concurrencia y el multiprocesamiento no están implementados.
- Algunas bibliotecas de Python pueden no tener equivalentes en Java.
