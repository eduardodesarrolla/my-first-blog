from django import forms
from . models import producto


class ProductoForm(forms.ModelForm):
    
    class Meta:
        model = producto
        
        fields = ["upc", "peso", "ancho", "altura", "largo"]