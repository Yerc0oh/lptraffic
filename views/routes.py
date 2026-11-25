import pandas as pd
import plotly.express as px
import streamlit as st
from src.utils import compatible_models, conditions, download, show_map
from src.traffic_graph import load_network, build_graph
from src.prediction import inputs, predict
from src.genetic_algorithm import optimize, cost
from src.config import ROUTE_COLORS, MUTED


def render():
    st.header("Optimización de rutas")
    nodes, edges = load_network()
    names = nodes.set_index("node_id").nombre.to_dict()
    labels = {
        r.edge_id: f"{r.edge_id} · {r.avenida}: {names[r.origen]} → {names[r.destino]}"
        for r in edges.itertuples()
    }
    with st.form("route_form"):
        a, b = st.columns(2)
        origin = a.selectbox("Origen", list(names), format_func=names.get)
        destination = b.selectbox(
            "Destino", list(names), index=19, format_func=names.get
        )
        cond = conditions("r")
        blocked = st.multiselect(
            "Tramos bloqueados", list(labels), format_func=labels.get
        )
        accidents = st.multiselect(
            "Tramos con accidentes", list(labels), format_func=labels.get
        )
        with st.expander("Parámetros del algoritmo genético"):
            a, b, c = st.columns(3)
            population = a.number_input("Población", 2, 300, 50)
            generations = b.number_input("Generaciones", 1, 500, 100)
            elite = c.number_input("Élite", 1, 299, 2)
            tournament = a.number_input("Torneo", 2, 300, 3)
            cross = b.slider("Cruce", 0.0, 1.0, 0.8)
            mutation = c.slider("Mutación", 0.0, 1.0, 0.15)
            seed = a.number_input("Semilla", 0, 2**31 - 1, 42)
        submit = st.form_submit_button("Optimizar ruta", type="primary")
    if submit:
        st.session_state.pop("route_result", None)
        try:
            a, b = compatible_models()
            pred = predict(
                inputs(edges, *cond, blocked=blocked, accidents=accidents), a, b
            ).rename(columns={"tramo_id": "edge_id"})
            g = build_graph(nodes, pred)
            bar = st.progress(0)
            result = optimize(
                g,
                origin,
                destination,
                population,
                generations,
                cross,
                mutation,
                elite,
                tournament,
                seed,
                lambda i, n: bar.progress(i / n),
            )
            st.session_state.route_result = (result, pred, g)
        except Exception as e:
            st.error(str(e))
    if "route_result" not in st.session_state:
        return
    result, pred, g = st.session_state.route_result
    hist = pd.DataFrame(result["history"])
    rows = []
    paths = []
    ref = cost(g, result["references"]["Dijkstra distancia"])
    colors = ROUTE_COLORS
    for label, path, color in [
        (f"Genética {i+1}", p, colors[i]) for i, p in enumerate(result["routes"])
    ] + [(k, p, MUTED) for k, p in result["references"].items()]:
        t = cost(g, path)
        rows.append(
            {
                "Ruta": label,
                "Tiempo (min)": t,
                "Distancia (km)": cost(g, path, "distancia_km"),
                "Diferencia vs referencia distancia (%)": 100 * (t - ref) / ref,
                "Nodos": " → ".join(names[n] for n in path),
                "Avenidas": " → ".join(
                    g[x][y]["avenida"] for x, y in zip(path, path[1:])
                ),
            }
        )
        paths.append((path, label, color))
    df = pd.DataFrame(rows)
    a, b, c, d = st.columns(4)
    a.metric("Mejor tiempo", f'{df.iloc[0]["Tiempo (min)"]:.2f} min')
    b.metric("Distancia", f'{df.iloc[0]["Distancia (km)"]:.2f} km')
    c.metric("Fitness", f"{hist.mejor_fitness.iloc[-1]:.4f}")
    d.metric("Ejecución", f'{result["seconds"]:.3f} s')
    st.write("**Mejor ruta:** " + df.iloc[0].Nodos)
    st.dataframe(df, use_container_width=True)
    show_map(nodes, pred, paths, key="route_map")
    st.plotly_chart(
        px.line(
            hist,
            x="generacion",
            y=["mejor_fitness", "fitness_promedio"],
            title="Evolución del fitness",
        ),
        use_container_width=True,
    )
    st.plotly_chart(
        px.line(hist, x="generacion", y="mejor_costo", title="Mejor costo (min)"),
        use_container_width=True,
    )
    st.caption(
        f"{len(hist)} generaciones · {hist.individuos_validos.iloc[-1]} individuos válidos en la última generación."
    )
    st.dataframe(hist)
    download(df, "Exportar rutas", "rutas.csv")
    download(hist, "Exportar generaciones", "generaciones.csv")
    st.info(
        "Dijkstra es óptimo con pesos fijos positivos y aditivos. El algoritmo genético explora soluciones y no garantiza superar esa referencia. Se mantienen condiciones constantes durante el recorrido."
    )
