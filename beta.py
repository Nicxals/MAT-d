import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import streamlit as st

ciudades_lista = ["Lima", "Piura", "Chiclayo", "Trujillo", "Iquitos", "Cusco", "Puerto Maldonado", "Juliaca", "Arequipa"]
posiciones = {
    "Lima": (0, 0), "Piura": (-1.5, 4), "Chiclayo": (-1.2, 3), "Trujillo": (-1, 2),
    "Iquitos": (2, 5), "Cusco": (3, -1.5), "Puerto Maldonado": (5, -1), "Juliaca": (4, -3), "Arequipa": (2.5, -4)
}

M = np.array([
    [0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 0]
])

M2 = np.linalg.matrix_power(M, 2)
M3 = np.linalg.matrix_power(M, 3)

colores_dict = {"Azul": "blue", "Rojo": "red", "Verde": "green"}

# --- Inicializar session_state ---
if "opciones" not in st.session_state:
    st.session_state.opciones = []
if "origen" not in st.session_state:
    st.session_state.origen = ""
if "destino" not in st.session_state:
    st.session_state.destino = ""

# --- Título ---
st.title("✈️ Simulador de Vuelos ")
st.markdown("Encuentra rutas entre ciudades del Perú .")

# --- Sidebar ---
st.sidebar.header("Selecciona tu vuelo")
origen = st.sidebar.selectbox("Ciudad de origen o mas cercana", ciudades_lista, index=0)
destino = st.sidebar.selectbox("Ciudad de destino", ciudades_lista, index=1)
color_nombre = st.sidebar.radio("Color de la ruta", ["Azul", "Rojo", "Verde"])
buscar = st.sidebar.button("Buscar rutas")

# --- Grafo completo inicial ---
st.subheader("Mapa de ciudades disponibles")
G_completo = nx.DiGraph()
G_completo.add_nodes_from(ciudades_lista)

fig0, ax0 = plt.subplots(figsize=(8, 6))
nx.draw_networkx_nodes(G_completo, posiciones, node_color="#AAAAAA", node_size=500, ax=ax0)
nx.draw_networkx_labels(G_completo, posiciones, font_size=8, font_weight="bold", ax=ax0)
ax0.set_title("Ciudades disponibles - Selecciona origen y destino")
ax0.grid(True, linestyle='--', alpha=0.3)
st.pyplot(fig0)

# --- Al presionar buscar, guardar resultados en session_state ---
if buscar:
    u = ciudades_lista.index(origen)
    v = ciudades_lista.index(destino)

    if u == v:
        st.warning("El origen y destino son la misma ciudad.")
        st.session_state.opciones = []
    else:
        opciones = []

        if M[u][v] == 1:
            opciones.append(("VUELO DIRECTO", [ciudades_lista[u], ciudades_lista[v]]))

        if M2[u][v] >= 1:
            for i in range(len(M)):
                if M[u][i] == 1 and M[i][v] == 1 and i != u and i != v:
                    opciones.append(("1 ESCALA", [ciudades_lista[u], ciudades_lista[i], ciudades_lista[v]]))
                    break

        if M3[u][v] >= 1:
            encontrado = False
            for i in range(len(M)):
                for j in range(len(M)):
                    if M[u][i] == 1 and M[i][j] == 1 and M[j][v] == 1 and i != u and i != v and j != u and j != v and i != j:
                        opciones.append(("2 ESCALAS", [ciudades_lista[u], ciudades_lista[i], ciudades_lista[j], ciudades_lista[v]]))
                        encontrado = True
                        break
                if encontrado:
                    break

        # Guardar en session_state
        st.session_state.opciones = opciones
        st.session_state.origen = origen
        st.session_state.destino = destino

# --- Mostrar resultados desde session_state ---
if st.session_state.opciones:
    color_final = colores_dict[color_nombre]
    opciones = st.session_state.opciones

    if not opciones:
        st.error("No existe ruta disponible entre estas ciudades.")
    else:
        st.subheader("Rutas disponibles")
        labels = [f"{info}: {' → '.join(ruta)}" for info, ruta in opciones]
        seleccion = st.radio("Elige una ruta para visualizar:", labels)
        idx = labels.index(seleccion)
        info, ruta = opciones[idx]

        st.success(f"Ruta seleccionada: {' → '.join(ruta)}")

        G_ruta = nx.DiGraph()
        G_ruta.add_nodes_from(ciudades_lista)
        for k in range(len(ruta) - 1):
            G_ruta.add_edge(ruta[k], ruta[k+1])

        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw_networkx_nodes(G_ruta, posiciones, node_color="#F70B0BFF", node_size=500, ax=ax)
        nx.draw_networkx_labels(G_ruta, posiciones, font_size=8, font_weight="bold", ax=ax)
        nx.draw_networkx_edges(G_ruta, posiciones, edge_color=color_final, width=2, arrowsize=20, connectionstyle='arc3,rad=0.1', ax=ax)
        ax.set_title(f"Ruta: {st.session_state.origen} → {st.session_state.destino}\n{info}")
        ax.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig)
