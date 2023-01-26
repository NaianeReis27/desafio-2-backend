from rest_framework import generics
from .serializers import TransactionsSerializers
from .models import Transactions
from django.shortcuts import render
import datetime

def formTransactions(request):
    transactions = Transactions.objects.all()
    if request.method == "POST":
        file =  request.FILES['document'].readlines()
        for ele in file:
            data_decoded = ele.decode('utf-8').replace("\r","").replace("\n","")
            date = datetime.date(int(data_decoded[1 : 5]), int(data_decoded[5 : 7]), int(data_decoded[7 : 9]) )
            time = datetime.time(int(data_decoded[42 : 44]), int(data_decoded[44 : 46]), int(data_decoded[46 : 48]) )
            data = {
                'type':  data_decoded[0 : 1],
                'data':  date,
                'value': round(int(data_decoded[10 : 19]), 2),
                'cpf':   data_decoded[19 : 30],
                'card':  data_decoded[30 : 42],
                'hour':  time,
                'owner': data_decoded[48 : 62],
                'store': data_decoded[62 : 81]
            }
            serializer = TransactionsSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
    return render(request, 'transactions/addFile.html', {'transactions': transactions} )
