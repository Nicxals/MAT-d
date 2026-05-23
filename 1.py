import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# 1. Configuración de datos y Nodos
ciudades_lista = ["Lima", "Piura", "Chiclayo", "Trujillo", "Iquitos", "Cusco", "Puerto Maldonado", "Juliaca", "Arequipa"]
posiciones = {
    "Lima": (0, 0), "Piura": (-1.5, 4), "Chiclayo": (-1.2, 3), "Trujillo": (-1, 2),
    "Iquitos": (2, 5), "Cusco": (3, -1.5), "Puerto Maldonado": (5, -1), "Juliaca": (4, -3), "Arequipa": (2.5, -4)
}


M = np.array([
    #Lm Pi Ch Tr Iq Cu PM Jl Ar
    [0, 1, 1, 1, 1, 1, 0, 1, 1], #Lima
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #Piura
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #Chiclayo
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #Trujillo
    [1, 0, 0, 0, 0, 0, 0, 0, 0], #Iquitos
    [1, 0, 0, 0, 0, 0, 1, 1, 1], #Cusco
    [0, 0, 0, 0, 0, 1, 0, 0, 0], #PuertoMaldonado
    [1, 0, 0, 0, 0, 1, 0, 0, 0], #Juliaca
    [1, 0, 0, 0, 0, 1, 0, 0, 0] #Arequipa
])


M2 = np.linalg.matrix_power(M, 2) 
M3 = np.linalg.matrix_power(M, 3)

colores_dict = {"1": "blue", "2": "red", "3": "green", "4": "orange", "5": "purple", "6": "black"}

while True:
    print("\n--- SIMULADOR DE VUELOS (MATRICES BOOLEANAS) ---")
    for i, ciudad in enumerate(ciudades_lista):
        print(f"{i+1} {ciudad}")
    print("0 para salir")
    orig = input("Escoja la estacion mas cercana o de origen ")
    if orig == "0": break
    dest = input("Escoger la estacion de Destino: ")
    col_op = input("Color (1:Azul, 2:Rojo, 3:Verde): ")

    if not (orig.isdigit() and dest.isdigit()) or int(orig) > 9 or int(dest) > 9:
        print("Error: Selección inválida.")
        continue

    # Ajustar índices para la matriz (0-8)
    u, v = int(orig) - 1, int(dest) - 1
    color_final = colores_dict.get(col_op, "black")


    ruta = []


    if M[u][v] == 1:
        info = "VUELO DIRECTO"
        ruta = [ciudades_lista[u], ciudades_lista[v]]
    elif M2[u][v] >= 1:
        info = "CONEXIÓN CON 1 ESCALA"
        for i in range(len(M)):
            if M[u][i] == 1 and M[i][v] == 1:
                ruta = [ciudades_lista[u], ciudades_lista[i], ciudades_lista[v]]
    elif M3[u][v] >= 1:
        info = "CONEXIÓN CON 2 ESCALAS"
        for i in range(len(M)):
            for j in range(len(M)):
                if M[u][i] == 1 and M[i][j] == 1 and M[j][v] == 1:
                    ruta = [ciudades_lista[u], ciudades_lista[i],ciudades_lista[j], ciudades_lista[v]]
                    break
    else:
        print("No existe ruta disponible en este sistema.")
        continue

    print(f"\nResultado: {' -> '.join(ruta)}")
    print(f"Estado: {info}")


    G_ruta = nx.DiGraph()
    G_ruta.add_nodes_from(ciudades_lista)
    for i in range(len(ruta)-1):
        G_ruta.add_edge(ruta[i], ruta[i+1])

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G_ruta, posiciones, node_color="#F70B0BFF", node_size=500)
    nx.draw_networkx_labels(G_ruta, posiciones, font_size=8, font_weight="bold")
    nx.draw_networkx_edges(G_ruta, posiciones, edge_color=color_final, width=2, arrowsize=20, connectionstyle='arc3,rad=0.1')
    
    plt.title(f"Ruta: {ciudades_lista[u]} a {ciudades_lista[v]}\n{info}")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()