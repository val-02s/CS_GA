import random
import copy
from typing import Dict, List
from CromosomaBin import CromosomaBinario
from interfaz import (Aptitud, Seleccion, Reproduccion, Mutacion,
                      AptitudMochila, SeleccionTorneo, ReproduccionUnCruce, MutacionFlip)


class GA(object):
    def __init__(self, num_inv: int, num_genes: int, hyperparams: Dict):
        self.poblacion: List[CromosomaBinario] = [CromosomaBinario(num_genes) for i in range(num_inv)]
        self.num_inv: int = num_inv
        self.hyperparams: Dict = hyperparams
        self.evaluar: Aptitud = hyperparams["Aptitud"]
        self.seleccion: Seleccion = hyperparams["Seleccion"]
        self.reproducion: Reproduccion = hyperparams["Reproduccion"]
        self.mutacion: Mutacion = hyperparams["Mutacion"]
        self.num_remplazo = int(hyperparams["por_remplazo"] * num_inv)
        self.mutar_elite: bool = hyperparams.get("mutar_elite", True)
        self.historial: Dict = {"mejor": [], "promedio": []}
        self.generaciones: int = 0
        for i in range(num_inv):
            self.poblacion[i].llenar_random_data()

    def buscar_solucion(self, tolerancia: float, var: Dict, max_generaciones: int = None,
                        paciencia: int = None, verbose: bool = True):
        avg_tol: float = 99999999.99
        sum_score_prev: float = 0
        sum_score: float = 1
        generacion: int = 1
        mating_pool = None
        generacion_nueva: List = None
        fail: bool = False
        fail_count: int = 0
        fail_score: float = 0.0
        mejor_global: float = float("-inf")
        sin_mejora: int = 0
        while not fail:
            self.evaluar.evaluar_poblacion(self.poblacion, var)
            sum_scores: float = sum([cromosoma.score for cromosoma in self.poblacion])
            sum_scores /= self.num_inv
            avg_tol = abs(sum_scores - sum_score_prev) / sum_score
            sum_score_prev = sum_scores
            mejor = max(c.score for c in self.poblacion)
            self.historial["mejor"].append(mejor)
            self.historial["promedio"].append(sum_scores)
            if mejor > mejor_global:
                mejor_global = mejor
                sin_mejora = 0
            else:
                sin_mejora += 1
            if verbose and (generacion + 1) % 100 == 0:
                print(f"[{generacion:04d}] avg_err : {avg_tol:.5f} avg_score: {sum_scores:.5f}")
            if fail_score == avg_tol:
                fail_count += 1
                if fail_count >= 10:
                    fail = True
                    break
            if avg_tol < tolerancia:
                break
            if max_generaciones is not None and generacion >= max_generaciones:
                break
            if paciencia is not None and sin_mejora >= paciencia:
                break
            fail_score = avg_tol
            self.poblacion = sorted(self.poblacion, key=lambda c: c.score, reverse=True)
            mating_pool = self.seleccion.seleccion_poblacion(self.poblacion)
            generacion_nueva = copy.deepcopy(self.poblacion[:self.num_remplazo])
            self.reproducion.reproduccion_poblacion(generacion_nueva, mating_pool, self.num_inv)
            if self.mutar_elite:
                self.mutacion.mutacion_poblacion(generacion_nueva)
            else:
                self.mutacion.mutacion_poblacion(generacion_nueva[self.num_remplazo:])
            generacion += 1
            self.poblacion = copy.deepcopy(generacion_nueva)
        self.generaciones = generacion


def sum_pesos_test(pesos, cromosoma):
    s = 0
    for i in range(cromosoma.n_genes):
        if cromosoma.get_bits(i + 1) == 1:
            s += pesos[i]
    return s


def optimo_dp(pesos, valores, capacidad):
    dp = [0] * (capacidad + 1)
    for p, v in zip(pesos, valores):
        for c in range(capacidad, p - 1, -1):
            dp[c] = max(dp[c], dp[c - p] + v)
    return dp[capacidad]


if __name__ == "__main__":
    random.seed(42)
    variables = {}
    variables["pesos"] = [random.randint(1, 10) for i in range(32)]
    variables["valores"] = [random.randint(10, 100) for i in range(32)]
    variables["capacidad"] = 80
    print("pesos:", variables["pesos"])
    print("valores:", variables["valores"])
    print("capacidad:", variables["capacidad"])
    num_genes = 32
    cant_ind = 100
    gaparams = {}
    gaparams["Aptitud"] = AptitudMochila()
    gaparams["Seleccion"] = SeleccionTorneo(3)
    gaparams["Reproduccion"] = ReproduccionUnCruce(num_genes)
    gaparams["Mutacion"] = MutacionFlip(0.05)
    gaparams["por_remplazo"] = 0.5
    random.seed(1)
    algoritmoGA = GA(cant_ind, num_genes, gaparams)
    algoritmoGA.buscar_solucion(1e-4, variables, max_generaciones=1000, paciencia=300)
    print(f"{'id':^6} {'Cromosoma':^32} Score")
    solucion = sorted(algoritmoGA.poblacion, key=lambda c: c.score, reverse=True)
    for i, cromosoma in enumerate(solucion):
        print(f"[{i + 1:^4d}] {cromosoma.bits:032b} : {cromosoma.score} -> {sum_pesos_test(variables['pesos'], cromosoma):4d} kg")
