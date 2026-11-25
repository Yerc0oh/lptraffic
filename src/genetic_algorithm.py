import random,time
import networkx as nx
import numpy as np

def valid(g,path,origin,destination):
    return bool(path) and path[0]==origin and path[-1]==destination and len(set(path))==len(path) and all(g.has_edge(a,b) for a,b in zip(path,path[1:]))

def random_path(g,a,b,rng,forbidden=()):
    seen=set(forbidden)-{a,b}; visited=set(seen); visited.add(a); path=[a]
    def dfs(u):
        if u==b: return True
        neighbors=list(g.successors(u)); rng.shuffle(neighbors)
        for v in neighbors:
            if v not in visited:
                visited.add(v); path.append(v)
                if dfs(v): return True
                path.pop()
        return False
    return path if dfs(a) else None

def crossover(g,p,q,rng):
    common=sorted(set(p[1:-1])&set(q[1:-1])); rng.shuffle(common)
    for n in common:
        child=p[:p.index(n)]+q[q.index(n):]
        if valid(g,child,p[0],p[-1]): return child
    return p.copy()

def mutate(g,p,rng):
    if len(p)<2: return p.copy()
    i,j=sorted(rng.sample(range(len(p)),2)); replacement=random_path(g,p[i],p[j],rng,p[:i]+p[j+1:])
    child=p[:i]+replacement+p[j+1:] if replacement else p.copy()
    return child if valid(g,child,p[0],p[-1]) else p.copy()

def cost(g,p,weight='tiempo_recorrido_min'):
    return sum(g[a][b][weight] for a,b in zip(p,p[1:]))

def optimize(
    g,
    origin,
    destination,
    population=50,
    generations=100,
    cross=0.8,
    mutation=0.15,
    elite=2,
    tournament=3,
    seed=42,
    callback=None,
):
    if origin == destination or origin not in g or destination not in g:
        raise ValueError("Origen y destino deben ser distintos y válidos.")
    if not (
        2 <= population <= 300
        and 1 <= generations <= 500
        and 1 <= elite < population
        and 2 <= tournament <= population
        and 0 <= cross <= 1
        and 0 <= mutation <= 1
    ):
        raise ValueError("Parámetros genéticos incompatibles.")
    if not nx.has_path(g, origin, destination):
        raise ValueError("No existe una ruta disponible.")
    if any(
        not np.isfinite(d.get("tiempo_recorrido_min", np.nan))
        or d["tiempo_recorrido_min"] <= 0
        for _, _, d in g.edges(data=True)
    ):
        raise ValueError("Pesos de tiempo inválidos.")
    rng = random.Random(seed)
    start = time.perf_counter()
    unique = {}
    for _ in range(population * 5):
        p = random_path(g, origin, destination, rng)
        if p:
            unique[tuple(p)] = p
        if len(unique) >= population:
            break
    pop = list(unique.values())
    pop += [rng.choice(pop).copy() for _ in range(population - len(pop))]
    archive = dict(unique)
    hist = []

    def rank(p):
        return cost(g, p)

    def select():
        return min(rng.sample(pop, tournament), key=rank)

    for generation in range(1, generations + 1):
        pop.sort(key=rank)
        next_pop = [p.copy() for p in pop[:elite]]
        while len(next_pop) < population:
            p = select()
            q = select()
            child = crossover(g, p, q, rng) if rng.random() < cross else p.copy()
            if rng.random() < mutation:
                child = mutate(g, child, rng)
            if valid(g, child, origin, destination):
                next_pop.append(child)
            else:
                next_pop.append(p.copy())
        pop = next_pop
        archive.update({tuple(p): p for p in pop})
        scores = [rank(p) for p in pop]
        best = min(scores)
        hist.append(
            dict(
                generacion=generation,
                mejor_costo=best,
                mejor_fitness=1 / (best + 1e-9),
                fitness_promedio=float(np.mean([1 / (s + 1e-9) for s in scores])),
                individuos_validos=len(pop),
                rutas_distintas=len(set(map(tuple, pop))),
            )
        )
        if callback:
            callback(generation, generations)
    return dict(
        routes=sorted(archive.values(), key=rank)[:3],
        history=hist,
        seconds=time.perf_counter() - start,
        references={
            "Dijkstra distancia": nx.shortest_path(
                g, origin, destination, weight="distancia_km"
            ),
            "Dijkstra tiempo": nx.shortest_path(
                g, origin, destination, weight="tiempo_recorrido_min"
            ),
        },
    )
