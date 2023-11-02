from django import forms
from .models import Order
from django.core.validators import MinLengthValidator, MaxLengthValidator

class OrderForm(forms.ModelForm):

    postal = forms.CharField(
        validators=[
            MinLengthValidator(limit_value=5, message='PSČ musí obsahovať 5 čísiel.'),
            MaxLengthValidator(limit_value=5, message='PSČ musí obsahovať 5 čísiel.'),
        ]
    )

    def clean_postal(self):
        postal = self.cleaned_data.get('postal')
        try:
            int(postal)  # Attempt to convert the value to an integer
        except ValueError:
            raise forms.ValidationError('PSČ musí byť číslo.')
        return postal

    class Meta:
        model = Order
        exclude = ['date_from', 'date_to', 'price', 'paid']
