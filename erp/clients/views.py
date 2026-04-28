from .models import Client
from django.shortcuts import render
from sales.models import Estimate   # ⭐ 이 줄도 추가
from django.contrib.auth.decorators import login_required

@login_required
def client_detail(request, pk):
    client = Client.objects.get(id=pk)
    estimates = Estimate.objects.filter(client=client)

    return render(request, 'clients/detail.html', {
        'client': client,
        'estimates': estimates
    })

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/list.html', {'clients': clients})