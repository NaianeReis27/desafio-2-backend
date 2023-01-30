from .serializers import TransactionsSerializers
from .models import Transactions
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
import datetime


def formTransactions(request):

    msg = []
    transactions = Transactions.objects.all()

    if request.method == "POST":
        if not request.FILES :
            msg.append({"msg": f"Não adicionou um arquivo", 'type': 'info'})
        else:
            if request.FILES['document'].content_type != "text/plain":
                msg.append({"msg": f"Formato inválido", 'type': 'info'})
            else :    
                file = request.FILES['document'].readlines()
                for index, ele in enumerate(file):
                    try:
                        data_decoded = ele.decode(
                            'utf-8').replace("\r", "").replace("\n", "")
                        date = datetime.date(int(data_decoded[1: 5]), int(
                            data_decoded[5: 7]), int(data_decoded[7: 9]))

                        time = datetime.time(int(data_decoded[42: 44]), int(
                            data_decoded[44: 46]), int(data_decoded[46: 48]))

                        if data_decoded[0: 1] == '2' or data_decoded[0: 1] == '3' or data_decoded[0: 1] == '9':
                            value = -int(data_decoded[10: 19])/100
                        else:
                            value = int(data_decoded[10: 19])/100

                        data = {
                            'type':  data_decoded[0: 1],
                            'data':  date,
                            'value': round(value, 2),
                            'cpf':   data_decoded[19: 30],
                            'card':  data_decoded[30: 42],
                            'hour':  time,
                            'owner': data_decoded[48: 62],
                            'store': data_decoded[62: 81]
                        }

                    except:
                        msg.append({ "msg": f"A linha {index + 1} não foi registrada", 'type': 'error'})
                        continue
                    
                    serializer = TransactionsSerializers(data=data)

                    if serializer.is_valid():
                        serializer.save()
                        msg.append({"msg": f"A linha {index + 1} foi registrada", 'type': 'sucess'})

    return render(request, 'transactions/home.html', {'transactions': transactions, "msg": msg})


def filter(request, store):

    if request.method == "GET":
        transactions = get_list_or_404(Transactions, store=store)
        soma = 0
        for transaction in transactions:
            soma = transaction.value + soma

    return render(request, 'transactions/store.html', {'transactions': transactions, 'soma': soma})
