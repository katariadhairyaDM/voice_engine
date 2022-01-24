from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
import numpy as np
from django.contrib.auth.models import User
from django.views.generic import View
from time import time
from .date_module import date_module
from .main import function
import copy


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def index(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            text = json.load(request)
            print(text)
            try:
                data = function(text)
            except:
                data = {'message': "Sorry, the Query couldn't be processed", 'make_graph': 'no'}
            print("This is data : ",data)
            # print("This is data2 : ",json.dumps(data2))
            # print("Data2 :")
            
            # data = {'message': ' ', 'make_graph': 'yes', 'graph_type': 'table', 'columns': [['number', 'Spend'], ['number', 'App Installs'], ['number', 'Cost Per App Installs']], 'rows': [[1953.75, 6, 325.625]]}
            # data = {'message': 'This is a data Campaign Example', 'make graph': 'yes', 'graph type': 'line', 'columns': [['string', 'Campaign Name'], ['number', 'Campaign Id'], ['number', 'Spend'], ['number', 'App Installs'], ['number', 'Cost Per App Installs']], 'rows': [['Moj - MFC | New Audience_2021/12/20', 6258656629335, 803.68, 2, 401.84], ['Moj - MFC | New Audience_2021/12/20', 6258656629335, 1953.75, 6, 325.625], ['Moj - MFC | New Audience_2021/12/20', 6258656629335, 799.15, 3, 266.383333]]}
            return JsonResponse(json.dumps(data, cls=NpEncoder), status=200, safe=False)
        
    return render(request, 'index.html')





# Your codes .... 

