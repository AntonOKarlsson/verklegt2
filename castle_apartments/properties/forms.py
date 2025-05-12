from django import forms
from .models import Property, PostalCode


class PropertyForm(forms.ModelForm):
    postal_code = forms.ModelChoiceField(
        queryset=PostalCode.objects.order_by("code"),
        to_field_name="code",
        empty_label="Select postal code",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Property
        fields = ('header_image', 'title', 'description', 'price', 'address', 'postal_code','property_type',
                  'num_rooms','num_bedrooms','num_bathrooms','size_sqm','built_year')
        labels = {
                    'size_sqm' : 'Size (m²)',
                    'num_rooms' : 'Number of rooms',
                    'num_bedrooms' : 'Number of bedrooms',
                    'num_bathrooms' : 'Number of bathrooms',
        }
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
            'built_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Year built'}),
        }
