from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Seller




class SignUpForm(UserCreationForm):
    #sérstakar þakkir fær github-userinn flatplanet fyrir hjálp í þessum kóda
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    is_seller = forms.BooleanField(required=False)
    profile_image = forms.ImageField(label="", required=False, widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_seller','profile_image', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        User = get_user_model()
        model = User
        fields = ['new_password1','new_password2']


class UpdateUserForm(UserChangeForm):
    #sérstakar þakkir fær github-userinn flatplanet fyrir hjálp í þessum kóda
    password = None
    #password stuff hidden for now
    email = forms.EmailField(label="Email address", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    is_seller = forms.BooleanField(required=False)
    profile_image = forms.ImageField(label="Profile Image", required=False)


    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_seller', 'profile_image',)

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = 'User name'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


class SellerForm(forms.ModelForm):
    class Meta:
        User = get_user_model()
        model = Seller
        fields = ['type', 'logo_url', 'cover_image_url', 'bio', 'agency_address']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Type'}),
            'logo_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Logo URL'}),
            'cover_image_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cover Image URL'}),
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
            'agency_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agency Address'}),
        }
