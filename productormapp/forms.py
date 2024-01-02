from productormapp.models import Product
from django.forms import ModelForm

class ViewProduct(ModelForm):
    class Meta:
        model=Product
        fields="__all__"