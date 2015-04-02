from django import forms
from webapp.models import Category,Purchase,Depart

class PurchaseForm(forms.ModelForm):
	class Meta:
		model = Purchase
		fields =('name', 'category', 'cost', 'depart', 'about')