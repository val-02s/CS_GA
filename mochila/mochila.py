import random
random.seed(1)
from itertools import product

pesos = [12, 2, 1, 1, 4]
valores = [4, 2, 2, 1, 10]
capacidad = 15
n = len(pesos)

tam_poblacion = 8
generaciones = 15
prob_mutacion = 0.1


def peso_de(c):
    return sum(p for p, g in zip(pesos, c) if g)


def aptitud(c):
    if peso_de(c) > capacidad:
        return 0
    return sum(v for v, g in zip(valores, c) if g)


def seleccion(poblacion):
    a, b = random.sample(poblacion, 2)
    return a if aptitud(a) >= aptitud(b) else b


def cruce(padre1, padre2):
    punto = random.randint(1, n - 1)
    return padre1[:punto] + padre2[punto:], padre2[:punto] + padre1[punto:]


def mutacion(c):
    return [1 - g if random.random() < prob_mutacion else g for g in c]


poblacion = [[random.randint(0, 1) for _ in range(n)] for _ in range(tam_poblacion)]

for gen in range(1, generaciones + 1):
    mejor = max(poblacion, key=aptitud)
    print(f"Generacion {gen}: mejor = {mejor}  valor = {aptitud(mejor)}  peso = {peso_de(mejor)} kg")
    nueva = [mejor]
    while len(nueva) < tam_poblacion:
        h1, h2 = cruce(seleccion(poblacion), seleccion(poblacion))
        nueva.append(mutacion(h1))
        if len(nueva) < tam_poblacion:
            nueva.append(mutacion(h2))
    poblacion = nueva

mejor = max(poblacion, key=aptitud)
print("\nSolucion del algoritmo genetico")
print("Cromosoma:", mejor)
print("Cajas elegidas:", [i + 1 for i, g in enumerate(mejor) if g])
print("Valor:", aptitud(mejor), " Peso:", peso_de(mejor), "kg")

optimo = max(aptitud(list(c)) for c in product([0, 1], repeat=n))
print("\nOptimo real (probando las 32 combinaciones):", optimo)
