from django.http import HttpResponse
from .models import Estimate
from .utils import generate_estimate_pdf
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EstimateForm, EstimateItemFormSet
from sales.models import Estimate
from django.contrib.auth.decorators import login_required

@login_required
def estimate_change_status(request, pk, status):
    estimate = get_object_or_404(Estimate, id=pk)
    estimate.status = status
    estimate.save()
    return redirect('/sales/')

@login_required
def estimate_update(request, pk):
    estimate = get_object_or_404(Estimate, id=pk)

    if request.method == 'POST':
        form = EstimateForm(request.POST, instance=estimate)
        formset = EstimateItemFormSet(request.POST, instance=estimate)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('/sales/')
    else:
        form = EstimateForm(instance=estimate)
        formset = EstimateItemFormSet(instance=estimate)

    return render(request, 'sales/update.html', {
        'form': form,
        'formset': formset
    })

@login_required
def client_detail(request, pk):
    client = Client.objects.get(id=pk)
    estimates = Estimate.objects.filter(client=client)

    return render(request, 'clients/detail.html', {
        'client': client,
        'estimates': estimates
    })

@login_required
def estimate_create(request):
    if request.method == 'POST':
        form = EstimateForm(request.POST)
        formset = EstimateItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            estimate = form.save()

            items = formset.save(commit=False)
            for item in items:
                item.estimate = estimate
                item.save()

            return redirect('/sales/')
    else:
        form = EstimateForm()
        formset = EstimateItemFormSet()

    return render(request, 'sales/create.html', {
        'form': form,
        'formset': formset
    })

@login_required
def estimate_list(request):
    estimates = Estimate.objects.all()
    return render(request, 'sales/list.html', {'estimates': estimates})

def estimate_pdf(request, pk):
    estimate = Estimate.objects.get(pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="estimate_{pk}.pdf"'

    generate_estimate_pdf(response, estimate)

    return response