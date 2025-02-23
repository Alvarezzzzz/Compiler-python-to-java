import numpy as np

def ingresar_arreglo(dimension):
    print(f"Ingrese los elementos del arreglo de {dimension} dimensiones:")
    arreglo = []
    for i in range(dimension):
        elemento = float(input(f"Elemento {i+1}: "))
        arreglo.append(elemento)
    return np.array(arreglo)

def operacion_elemental(a, X, b, Y):
    return a * X + b * Y

def main():
    # Solicitar la dimensión de los arreglos
    dimension = int(input("Ingrese la dimensión de los arreglos: "))
    
    # Ingresar los arreglos X e Y
    print("Arreglo X:")
    X = ingresar_arreglo(dimension)
    
    print("Arreglo Y:")
    Y = ingresar_arreglo(dimension)
    
    # Ingresar las constantes a y b
    a = float(input("Ingrese la constante a: "))
    b = float(input("Ingrese la constante b: "))
    
    # Realizar la operación elemental aX + bY
    resultado = operacion_elemental(a, X, b, Y)
    
    # Mostrar el resultado
    print("El resultado de aX + bY es:")
    print(resultado)

if __name__ == "__main__":
    main()