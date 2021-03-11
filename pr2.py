import json
import networkx as nx # для взаимодействия с графом
import matplotlib.pyplot as plt # для визуализации графа

def print_table(table):
    i = 1
    shift = '-'*(8*len(table[0]) + 3)
    print(shift)
    print('\t1',end='\t')
    for j in range(1, len(table[0])):
        print(j + 1,end='\t')
    print()
    print(shift)
    for row in table:
        print(i, ' |', end='\t')
        for v in row:
            print(v, end='\t')
        print()
        i += 1
    print(shift, end='\n\n')


#построение таблицы с оценками критериев
def build_rate_table(table, tendencies, weights, borders):
    i = 0
    j = 0
    while i < len(table):
        while j < len(table[i]):
            if table[i][j] < borders[j][0]:
                if tendencies[j] < 0: # ниже средней шкалы
                    table[i][j] = weights[j] * 3
                else:
                    table[i][j] = weights[j]
            elif table[i][j] > borders[j][1]: # выше средней шкалы
                if tendencies[j] < 0:
                    table[i][j] = weights[j]
                else:
                    table[i][j] = weights[j] * 3
            else:
                table[i][j] = weights[j] * 2 # попадание в среднюю шкалу
            j += 1
        j = 0
        i += 1


def build_ratio_matrix(table, weights):
    matrix = [['X' for _ in range(len(table))] for _ in range(len(table))]

    i = 0
    j = 0
    while i < len(matrix):
        j = 0
        while j < i:
            if not isinstance(matrix[i][j], float) and matrix[i][j] not in ['N', 'inf']:
                res, value = compare_alt(i, j, table, weights)
                if res == i:
                    matrix[i][j] = value
                    matrix[j][i] = 'N' 
                else:
                    matrix[j][i] = value
                    matrix[i][j] = 'N' 
            j += 1
        i += 1
    
    return matrix


#сравнение двух альтернатив, возвращает индекс доминирующей и полученное отношение
def compare_alt(dominant, suppressed, table, weights):
    P_ij = 0
    N_ij = 0
    P_ji = 0
    N_ji = 0

    i = 0
    while i < len(table[dominant]):
        if table[dominant][i] > table[suppressed][i]:
            P_ij += weights[i]
            N_ji += weights[i]
        elif table[dominant][i] < table[suppressed][i]:
            N_ij += weights[i]
            P_ji += weights[i]
        i += 1

    if N_ij == 0:
        return dominant, 'inf'
    elif N_ji == 0:
        return suppressed, 'inf'
    
    D_ij = round(P_ij / N_ij, 2)
    D_ji = round(P_ji / N_ji, 2)

    return (dominant, D_ij) if D_ij > 1 else (suppressed, D_ji)


def build_graph(matrix, C):
    filtered_matrix = [[] for _ in range(len(matrix))]

    # фильтруем пороговые значения
    i = 0
    while i < len(matrix):
        for el in matrix[i]:
            if isinstance(el, float):
                filtered_matrix[i].append(el if el > C else 'N')
            else:
                filtered_matrix[i].append(el)
        i += 1

    G = nx.DiGraph()
    G.add_nodes_from(range(1, 10))
    i = 0
    j = 0
    while i < len(filtered_matrix):
        j = 0
        while j < len(filtered_matrix):
            if isinstance(filtered_matrix[i][j], float) or filtered_matrix[i][j] == 'inf':
                G.add_edge(i + 1, j + 1)
            j += 1
        i += 1
    pos = nx.shell_layout(G)
    nx.draw_networkx_edges(G, pos, arrowstyle='->')
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='#ffed00')
    nx.draw_networkx_labels(G, pos)
    plt.axis('off')
    plt.show()


with open('pr2_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    data = content["data"]
    tendencies = content["comp_markers"] #направления воозрастаний критериев
    weights = content["weights"]
    borders = content["borders"]

    table = [list(data[i].values())[1:] for i in range(len(data))]

    print_table(table)
    build_rate_table(table, tendencies, weights, borders)
    print_table(table)
    matrix = build_ratio_matrix(table, weights)
    print_table(matrix)
    build_graph(matrix, 1.7)
