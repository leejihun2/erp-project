from django import forms
from .models import Estimate
from django.forms import inlineformset_factory
from .models import Estimate, EstimateItem

EstimateItemFormSet = inlineformset_factory(
    Estimate,
    EstimateItem,
    fields=('name', 'price', 'quantity'),
    extra=3,
    can_delete=True
)

class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['client', 'title', 'amount', 'status']