import random
from itertools import product

valores_base = [4, 2, 2, 1, 10]
tam_poblacion = 8
generaciones = 15
prob_mutacion = 0.1


def correr(pesos, valores, capacidad, semilla):
    random.seed(semilla)
    n = len(pesos)

    def peso_de(c):
        return sum(p for p, g in zip(pesos, c) if g)

    def aptitud(c):
        if peso_de(c) > capacidad:
            return 0
        return sum(v for v, g in zip(valores, c) if g)

    def seleccion(poblacion):
        a, b = random.sample(poblacion, 2)
        return a if aptitud(a) >= aptitud(b) else b

    def cruce(p1, p2):
        punto = random.randint(1, n - 1)
        return p1[:punto] + p2[punto:], p2[:punto] + p1[punto:]

    def mutacion(c):
        return [1 - g if random.random() < prob_mutacion else g for g in c]

    poblacion = [[random.randint(0, 1) for _ in range(n)] for _ in range(tam_poblacion)]
    historial = []
    for gen in range(1, generaciones + 1):
        mejor = max(poblacion, key=aptitud)
        historial.append((gen, mejor, aptitud(mejor), peso_de(mejor)))
        nueva = [mejor]
        while len(nueva) < tam_poblacion:
            h1, h2 = cruce(seleccion(poblacion), seleccion(poblacion))
            nueva.append(mutacion(h1))
            if len(nueva) < tam_poblacion:
                nueva.append(mutacion(h2))
        poblacion = nueva
    mejor = max(poblacion, key=aptitud)
    optimo = max(aptitud(list(c)) for c in product([0, 1], repeat=n))
    return mejor, aptitud(mejor), peso_de(mejor), optimo, historial


escenarios = [
    ("Base", [12, 2, 1, 1, 4], 15),
    ("Capacidad 5 kg", [12, 2, 1, 1, 4], 5),
    ("Capacidad 10 kg", [12, 2, 1, 1, 4], 10),
    ("Capacidad 20 kg", [12, 2, 1, 1, 4], 20),
    ("Pesos [6, 3, 2, 5, 4]", [6, 3, 2, 5, 4], 15),
    ("Pesos [12, 8, 7, 9, 10]", [12, 8, 7, 9, 10], 15),
]

if __name__ == "__main__":
    for nombre, pesos, cap in escenarios:
        mejor, val, peso, opt, h = correr(pesos, valores_base, cap, 1)
        aciertos = sum(1 for s in range(100) if correr(pesos, valores_base, cap, s)[1] == opt)
        cajas = [i + 1 for i, g in enumerate(mejor) if g]
        print(f"{nombre} | cap {cap} | cromosoma {mejor} | cajas {cajas} | valor {val} | peso {peso} | optimo {opt} | aciertos {aciertos}/100")
