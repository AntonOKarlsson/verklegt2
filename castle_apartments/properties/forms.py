from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('header_image', 'title', 'description', 'price', 'address', 'postal_code','property_type',
                  'num_rooms','num_bedrooms','num_bathrooms','size_sqm','built_year')
        widgets = {
            'header_image': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'property_type': forms.TextInput(attrs={'class': 'form-control'}),
            'num_rooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of rooms'}),
            'num_bedrooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of bedrooms'}),
            'num_bathrooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of bathrooms'}),
            'size_sqm': forms.TextInput(attrs={'class': 'form-control'}),
            'built_year': forms.TextInput(attrs={'class': 'form-control'}),
        }
