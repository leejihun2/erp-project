from django.shortcuts import render
from sales.models import Estimate
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    total_count = Estimate.objects.count()
    total_amount = Estimate.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    draft_count = Estimate.objects.filter(status='draft').count()
    confirmed_count = Estimate.objects.filter(status='confirmed').count()
    completed_count = Estimate.objects.filter(status='completed').count()

    return render(request, 'dashboard.html', {
        'total_count': total_count,
        'total_amount': total_amount,
        'draft_count': draft_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
    })