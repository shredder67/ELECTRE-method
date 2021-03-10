import json
import matplotlib # для визуализации графа

#построение таблицы с оценками критериев
def build_rate_table(table):
    pass

def build_ratio_matrix(table):
    pass

def build_graph(table):
    pass

#сравнение двух альтернатив
def compare_alt(alt1, alt2, table):
    pass

#расчет индексов согласия для ЭЛЕКТРА-II
def calc_index(P_dominant, P_eq, P_sub):
    pass


with open('pr2_data.json', encoding='utf-8') as json_file:
    content = json.load(json_file)
    data = content["data"] 
    tendencies = content["comp_markers"] #направления воозрастаний критериев