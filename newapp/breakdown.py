import numpy as np
dic = {
    "object" : 'string',
    "float64" : 'number',
    "int64" : 'number'
}

def breakdown(df, query):
    x = df.groupby(['Publisher Placements'], as_index = False).sum()
    x['spend/install'] = x['Spend']/x['App Installs']
    x.drop(['Spend', 'App Installs'], axis='columns', inplace=True)
    x.replace([np.inf, -np.inf], 0, inplace=True)

    # getting the output ready to return

    output = {"message": query,
            "make_graph":"yes",
            "graph_type":"combo"
            }

    lst = []
    colm = x.columns
    for i in range(len(x.columns)):
        lst.append([dic[str(x[colm[i]].dtypes)], colm[i]])
    output['columns'] = lst

    rows = []
    for i in range(len(x)):
        row = []
        for j in range(len(x.columns)):
            row.append(x.iloc[i,j])
        rows.append(row)
    output['rows'] = rows

    return output