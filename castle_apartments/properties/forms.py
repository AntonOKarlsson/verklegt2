from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('header_image', 'title', 'description', 'price', 'address', 'postal_code','property_type',
                  'num_rooms','num_bedrooms','num_bathrooms','size_sqm','built_year')
        widgets = {
            'header_image': forms.TextInput(attrs={'class': 'form-control','placeholder':'Header image'}),
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Title'}),
            'description': forms.TextInput(attrs={'class': 'form-control','placeholder':'Description'}),
            'price': forms.TextInput(attrs={'class': 'form-control','placeholder':'Price'}),
            'address': forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control','placeholder':'Postal code'}),
            'property_type': forms.TextInput(attrs={'class': 'form-control','placeholder':'Property type'}),
            'num_rooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of rooms'}),
            'num_bedrooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of bedrooms'}),
            'num_bathrooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of bathrooms'}),
            'size_sqm': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Size (m²)'}),
            'built_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Built year'}),
        }
