# Dividing the query according to ad, adset, Campaign

def get_level_old(query):
    query_words = query.split(' ')

    if 'ad' in query_words or 'add' in query_words:
        return ['Ad Name', 'Ad Id', 'Adset Name', 'Adset Id', 'Campaign Name', 'Campaign Id', 'Spend', 'App Installs', 'Cost Per App Installs', 'Start Date'], 'Ad Id'
        # op = insights(df[['Campaign Name', 'Campaign Id', 'Adset Name', 'Adset Id', 'Ad Name', 'Ad Id', 'Spend', 'App Installs', 'Cost Per App Installs']], query_words, query)
    elif 'adset' in query_words:
        return ['Adset Name', 'Adset Id', 'Campaign Name', 'Campaign Id', 'Spend', 'App Installs', 'Cost Per App Installs', 'Start Date'], 'Adset Id'
        # op = insights(df[['Campaign Name', 'Campaign Id', 'Adset Name', 'Adset Id', 'Spend', 'App Installs', 'Cost Per App Installs']], query_words, query)
    else:
        return ['Campaign Name', 'Campaign Id', 'Spend', 'App Installs', 'Cost Per App Installs', 'Start Date'], 'Campaign Id'
        # op = insights(df[['Campaign Name', 'Campaign Id', 'Spend', 'App Installs', 'Cost Per App Installs']], query_words, query)

def GetLevel(query):
    query_words = query.split(' ')
    if 'account' in query_words:    
        return 'account'
    elif 'campaign' in query_words:
        return 'campaign'
    elif 'adset' in query_words:
        return 'adset'
    elif 'ad' in query_words or 'add' in query_words:
        return 'ad'
    elif 'placement' in query_words or 'platform' in query_words:
        return 'placement'
    else:
        return 'default'
        
def GroupBy(table_name, level_name):
    if table_name == 'placement':
        return ['Publisher Placements']
    elif table_name == 'insights':
        if level_name == 'ad':
            return ['Ad Id', 'Ad Name', 'Adset Id', 'Adset Name', 'Campaign Id', 'Campaign Name']
        # op = insights(df[['Campaign Name', 'Campaign Id', 'Adset Name', 'Adset Id', 'Ad Name', 'Ad Id', 'Spend', 'App Installs', 'Cost Per App Installs']], query_words, query)
        elif level_name == 'adset':
            return ['Adset Id', 'Adset Name', 'Campaign Name', 'Campaign Id']
            # op = insights(df[['Campaign Name', 'Campaign Id', 'Adset Name', 'Adset Id', 'Spend', 'App Installs', 'Cost Per App Installs']], query_words, query)
        elif level_name == 'campaign':
            return ['Campaign Id', 'Campaign Name']
        # op = insights(df[['Campaign Name', 'Campaign Id', 'Spend', 'App Installs', 'Cost Per App Installs']], query_words, query)
        else:
            return ['Account Name', 'Campaign Id', 'Campaign Name']

def GetDateFlag(table_name):
    if table_name == 'placement':
        return False
    elif table_name == 'insights':
        return True


column_substitute_map = {
    'Spend' : ['spend', 'spent'],

    'App Installs' : ['conversion', 'app', 'conversions', 'result metr', 'result matr'],

    'Cost Per App Installs' :['cost per conversion', 'cost per app install', 'cost per result', 'cost', 'publisher', 'placement'],

}
def GetFields(query, default_fields):
    final_fields = []
    for col in default_fields:
        lst = column_substitute_map[col]
        for ele in lst:
            if ele in query:
                final_fields.append(col)
                break
    if len(final_fields) == 0:
        final_fields = ['Spend']
    return final_fields


dis = {
    'top' : ['top'],
    'total' : ['much', 'many', 'total', 'sum'],
    'maximum' : ['max', 'maximum', 'best'],
    'minimum' : ['min', 'minimum', 'worst'],
    'daily' : ['daily', 'breakdown', 'trend']
}
def GetIntent(query, fields):
    reverse = False
    if 'Cost Per App Installs' == fields[0]:
        reverse = True
        
    for intent, val in dis.items():
        for ele in val:
            if ele in query:
                return intent, reverse
    return 'nointent', reverse