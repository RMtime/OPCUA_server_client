import pandas as pd
import graphviz as g
from tqdm import tqdm
import os.path as p


def create_tree(dataframe, gname):
    dot = g.Digraph(strict=True)
    dot.attr("node", fontname="SimSun", fontsize='12', shape='box')
    dot.attr(rankdir="LR")
    for i in dataframe.iterrows():
        for h in range(6):
            if i[1].values[h] != 'x':
                dot.node(i[1].values[h])
                if h >= 1:
                    dot.edge(i[1].values[h - 1], i[1].values[h])
    dot.render(f"./tree/{gname}", view=True)


def df_deal(path):
    df = pd.read_excel(path
                       , sheet_name=0, index_col=0)
    count = 0
    df1 = pd.DataFrame(data={"index": [i for i in range(df.shape[0])]})
    # print(df1.head())
    for item in df.iterrows():
        
        deal = item[1].values[0]
        deal = str(deal)
        lst = deal.split(">")
        for i in range(len(lst)):
            df1.loc[df1['index'] == count, f'level{i}'] = lst[i]
        count += 1
    df1.set_index("index", inplace=True)
    df1.drop(df1[df1["level1"] == "四期"].index, axis=0, inplace=True)
    hashable = df1.groupby("level0")
    count1 = 0
    for name, dtf in tqdm(hashable):
        count1 += 1
        dtf.fillna("x", inplace=True)
        if '*' in name:
            name = str(name).replace('*', '※')
        create_tree(dtf, name)
    print(count1)
    # df1.to_excel("test1.xlsx")


if __name__ == '__main__':
    path1 = 'C:/Users/admin/Desktop/点位.xlsx'
    df_deal(path1)
