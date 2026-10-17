import random
from GAbin import GA, sum_pesos_test, optimo_dp
from interfaz import AptitudMochila, SeleccionTorneo, ReproduccionUnCruce, MutacionFlip


def instancia(rango_pesos=(1, 10), capacidad=80):
    random.seed(42)
    pesos = [random.randint(*rango_pesos) for _ in range(32)]
    valores = [random.randint(10, 100) for _ in range(32)]
    return {"pesos": pesos, "valores": valores, "capacidad": capacidad}


def correr(var, semilla=1, recortar=True):
    random.seed(semilla)
    params = {"Aptitud": AptitudMochila(70, recortar), "Seleccion": SeleccionTorneo(3),
              "Reproduccion": ReproduccionUnCruce(32), "Mutacion": MutacionFlip(0.05),
              "por_remplazo": 0.5}
    ga = GA(100, 32, params)
    ga.buscar_solucion(1e-4, var, verbose=False, max_generaciones=1000, paciencia=300)
    mejor = max(ga.poblacion, key=lambda c: c.score)
    return mejor.score, sum_pesos_test(var["pesos"], mejor), optimo_dp(var["pesos"], var["valores"], var["capacidad"])


pruebas = [
    ("Base 80 kg", instancia(), 1, True),
    ("Capacidad 20 kg (original)", instancia(capacidad=20), 1, True),
    ("Capacidad 20 kg (sin recorte)", instancia(capacidad=20), 1, False),
    ("Capacidad 40 kg", instancia(capacidad=40), 1, True),
    ("Capacidad 120 kg", instancia(capacidad=120), 1, True),
    ("Capacidad 160 kg", instancia(capacidad=160), 1, True),
    ("Pesos 1 a 5", instancia(rango_pesos=(1, 5)), 1, True),
    ("Pesos 5 a 15", instancia(rango_pesos=(5, 15)), 1, True),
    ("Pesos 10 a 30 (original)", instancia(rango_pesos=(10, 30)), 1, True),
    ("Pesos 10 a 30 (sin recorte)", instancia(rango_pesos=(10, 30)), 1, False),
]
for semilla in range(2, 7):
    pruebas.append((f"Base 80 kg, semilla {semilla}", instancia(), semilla, True))

print(f"{'Prueba':<34}{'Score AG':>9}{'Peso':>6}{'Optimo':>8}")
for nombre, var, semilla, recortar in pruebas:
    score, peso, opt = correr(var, semilla, recortar)
    print(f"{nombre:<34}{score:>9}{peso:>6}{opt:>8}")
