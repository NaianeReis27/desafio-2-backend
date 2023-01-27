from .serializers import TransactionsSerializers
from .models import Transactions
from django.shortcuts import render , get_list_or_404
from django.http import HttpResponse
import datetime

def formTransactions(request):
    transactions = Transactions.objects.all()
    
    
    if request.method == "POST":

        if request.FILES['document'].content_type != "text/plain":
            return HttpResponse('formato invalido')

        file = request.FILES['document'].readlines()

        for index, ele in enumerate(file):
            print(ele,index)
            try:
                data_decoded = ele.decode(
                        'utf-8').replace("\r", "").replace("\n", "")
                date = datetime.date(int(data_decoded[1: 5]), int(
                        data_decoded[5: 7]), int(data_decoded[7: 9]))
                time = datetime.time(int(data_decoded[42: 44]), int(
                        data_decoded[44: 46]), int(data_decoded[46: 48]))

                data = {
                        'type':  data_decoded[0: 1],
                        'data':  date,
                        'value': round(int(data_decoded[10: 19]), 2),
                        'cpf':   data_decoded[19: 30],
                        'card':  data_decoded[30: 42],
                        'hour':  time,
                        'owner': data_decoded[48: 62],
                        'store': data_decoded[62: 81]
                }

            except:
                return HttpResponse(f'O arquivo não esta com a formatação correta na linha {index + 1}')

            serializer = TransactionsSerializers(data=data)

            if serializer.is_valid():
                serializer.save()

    return render(request, 'transactions/addFile.html', {'transactions': transactions})

def filter(request, store):
   
    if request.method == "GET":
        transactions = get_list_or_404(Transactions, store = store)
        soma = 0
        for transaction in transactions :
            soma = transaction.value + soma

    return render(request, 'transactions/list.html', {'transactions': transactions, 'soma': soma})
