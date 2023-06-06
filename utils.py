import seaborn as sns
import matplotlib.pyplot as plt

# 막대 그래프 그리기
def draw(x,y):
    ax = sns.barplot(x=x, y=y)

    # y축 값 그래프 위에 표현.
    for p in ax.patches:
        ax.annotate(
            format(p.get_height(), '.2f'), 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', va = 'center', 
            xytext = (0, -5), 
            textcoords = 'offset points',
        )
    
    # x축 라벨 비스듬히 기울이기
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right')
    return ax


import pickle

def get_pickle(file_pickle):
    with open(file_pickle, "rb") as file:
        restored_data = pickle.load(file)
    return restored_data


def classify(properties):
    properties_Filter, properties_Repository = [], []
    for item in properties:
        if 'Filter' in item['class-logging']:
            properties_Filter.append(item)
        elif 'Repository' in item['class-logging']:
            properties_Repository.append(item)
    
    return {
        'filter': properties_Filter,
        'repository': properties_Repository,
    }
