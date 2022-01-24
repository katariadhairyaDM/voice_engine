
from .insights import insights, output_function
from .date_module import date_module
from .breakdown import breakdown
from .select_table import select_table
from .get import GetDateFlag, GetFields, GetIntent, GetLevel, GroupBy
from .chatbot import ChatBot

def function(ip):
    query = ip['payload']
    accName = ip['accName']
    resultMetric = ip['resultMetric']
    CPR = ip['CPR']
    # CPI = ip['CPI']
    query = query.lower()
    
    messg = ChatBot(query)
    if messg:
        return output_function(messg, 'no', '', [])

    default_fields = ['Spend', resultMetric, CPR]

    # Selecting the datafram which will be used to get the required data
    datafram, table_name = select_table(query)
    print(table_name)
    if table_name == 'placement':
        return breakdown(datafram, query)

    # selecting the level (ad, adset, campaign)
    level_name = GetLevel(query)
    print(level_name)

    # Getting the groupby columns
    column_names= GroupBy(table_name, level_name)
    print(column_names)

    date_flag = GetDateFlag(table_name)
    dates = date_module(query)
    print(dates, date_flag)

    # Get the column to perform the operation
    fields = GetFields(query, default_fields)
    print(fields)

    # Get the operations
    intent, reverse = GetIntent(query, fields)
    print(intent, reverse)

    op = insights(datafram, query, column_names, date_flag, dates, fields, intent, reverse, resultMetric, CPR)

    if not op:
        op =  output_function("The query couldn't be processed, Please provide a valid query", 'no', '', [])

    op_dic = {
        'input query' : query,
        'table_name' : table_name,
        'level_name' : level_name,
        'column_names' : column_names,
        'dates' : dates,
        'fields': fields,
        'intent' : intent,
        'Output' : op
    }
    
    path = "E:/saved programs/django/project3/newapp/file.txt"
    f = open(path, 'a')
    f.write(str(op_dic))
    f.close()
    return op

if __name__ == '__main__':
    print(function({'payload': 'hi', 'accName': 'Moj-App Campaigns(300301992)', 'resultMetric': 'App Installs', 'CPR': 'Cost Per App Installs', 'CPI': 'EMAIL**'}))
