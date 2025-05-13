from django import forms
from .models import Property, PostalCode
from property_images.models import PropertyImage
from django.forms import modelformset_factory

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('title', 'description', 'price', 'address', 'postal_code','property_type',
                  'num_rooms','num_bedrooms','num_bathrooms','size_sqm','built_year')
        labels = {
                    'size_sqm' : 'Size (m²)',
                    'num_rooms' : 'Number of rooms',
                    'num_bedrooms' : 'Number of bedrooms',
                    'num_bathrooms' : 'Number of bathrooms',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Title'}),
            'description': forms.TextInput(attrs={'class': 'form-control','placeholder':'Description'}),
            'price': forms.TextInput(attrs={'class': 'form-control','placeholder':'Price'}),
            'address': forms.TextInput(attrs={'class': 'form-control','placeholder':'Address'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 105'}),
            'property_type': forms.TextInput(attrs={'class': 'form-control','placeholder':'Property type'}),
            'num_rooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of rooms'}),
            'num_bedrooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of bedrooms'}),
            'num_bathrooms': forms.TextInput(attrs={'class': 'form-control','placeholder':'Number of bathrooms'}),
            'size_sqm': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Size (m²)'}),
            'built_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Year built'}),
        }

PropertyImageFormSet = modelformset_factory(
    PropertyImage,
    fields=('image', 'is_thumbnail'),
    extra=3,
    widgets={
        'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': False}),
        'is_thumbnail': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
)