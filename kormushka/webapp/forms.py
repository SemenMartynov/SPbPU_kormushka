from django import forms
from webapp.models import Purchase

class PurchaseForm(forms.ModelForm):
	class Meta:
		model = Purchase
