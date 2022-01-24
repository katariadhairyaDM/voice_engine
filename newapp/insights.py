import pandas as pd
import numpy as np

l_str = [
        "Account Name",
        "Account Currency",
        "Account Id",
        "Attribution Settings",
        "Campaign Name",
        "Campaign Id",
        "Objective",
        "Buying Type",
        "Adset Name",
        "Adset Id",
        "Ad Name",
        "Ad Id",
        "Conversion Rate Ranking",
        "Engagement Rate Ranking",
        "Quality Ranking"
    ]


def insights(datafram, query, column_names, date_flag, dates, fields, intent, reverse, resultMetric, CPR):
    df = datafram
    if date_flag == True:
        datafram['Start Date'] = pd.to_datetime(datafram['Start Date'], format="%Y-%m-%d", exact=False)
        datafram['Stop Date'] = pd.to_datetime(datafram['Stop Date'], format="%Y-%m-%d", exact=False)
        df = datafram.loc[(datafram['Start Date'] >= dates[0]) & (datafram['Stop Date'] <= dates[1])]
        df = df.drop(['Stop Date'], axis=1)

    columns = df.columns
    for ele in columns:
        if ele in l_str:
            df[ele] = df[ele].apply(str)

    if intent != 'daily':
        print('hello')
        df = df.drop(['Start Date'], axis = 1)
        df = df.groupby(column_names, as_index = False).sum()
        df[CPR] = df['Spend']/df[resultMetric]
        df.replace([np.inf, -np.inf], 0, inplace=True)

    df = df.sort_values(by=fields, ascending = reverse)
    if intent == 'total':
        messg = 'The total {0} is {1} for time interval {2} - {3}....'.format(fields[0], str(df[fields[0]].sum()), str(dates[0]), str(dates[1]))
        x = []
        return output_function(messg, 'no', '', x)
    elif intent == 'maximum':
        messg = 'Maximum {0} for time interval {1} - {2}....'.format(fields[0], str(dates[0]), str(dates[1]))
        x = df.head(1)
        return output_function(messg, 'yes', 'table', x)     
    elif intent == 'minimum':
        messg = 'Minimum {0} for time interval {1} - {2}....'.format(fields[0], str(dates[0]), str(dates[1]))
        x = df.tail(1)
        return output_function(' ', 'yes', 'table', x)
    elif intent == 'top':
        query_words = query.split(' ')
        messg = 'Top {0} for time interval {1} - {2}....'.format(fields[0], str(dates[0]), str(dates[1]))
        ind = query_words.index('top')
        n = int(query_words[ind+1])
        x = df.head(n)
        return output_function(messg, 'yes', 'table', x)
    elif intent == 'daily':
        messg = 'Daily breakdown for {0} for time interval {1} - {2}....'.format(fields[0], str(dates[0]), str(dates[1]))
        colm = df.columns.tolist()
        colm.remove('Start Date')
        colm.remove(fields[0])
        colm.insert(0, fields[0])
        colm.insert(0, 'Start Date')
        print(colm)
        df = df[colm]
        x = df.groupby(['Start Date'], as_index = False).sum()
        return output_function(messg, 'yes', 'line', x)


    return output_function("The query couldn't be processed, Please provide a valid query", 'no', 'table', [])



# Getting the output ready to pass to Front end
dic = {
    "object" : 'string',
    "float64" : 'number',
    "int64" : 'number',
    'datetime64[ns]': 'string',
    'string' : 'string'
}

def output_function(messg, graph, graph_type, x):
    output = {}
    output['message'] = messg
    output['make_graph'] = graph
    output['graph_type'] = graph_type

    if len(x)!=0:
        lst = []
        colm = x.columns
        if 'Start Date' in colm:
            x['Start Date'] = x['Start Date'].dt.strftime('%Y-%m-%d')
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
    else:
        output['columns'] = []
        output['rows'] = []

    return output


if __name__ == '__main__':
    insights()