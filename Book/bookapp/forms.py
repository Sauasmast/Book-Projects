from django import forms
from django.forms import ModelForm
from .models import Sell_book, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UserChangeForm

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}), required= True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Your Email Address'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required= True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required= True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            # 'profile_image',
                )
        
    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['last_name']
        # user.profile_image = self.clean_data['profile_image']

        if commit:
            user.save()
        
        return user
    
class Editprofile(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}), required= True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Your Email Address'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required= True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required= True)
    profile_pic = forms.ImageField(required=False, help_text='Include an image of square size (Example: 250 by 250).')
    

class Sell_form(ModelForm):

    yesno_choices = (
    ('Yes','Yes'),
    ('No', 'No')
)
    book_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Book Title'}))
    isbn_no = forms.IntegerField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'ISBN No.'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Author FullName'}))
    price = forms.IntegerField(widget= forms.TextInput(attrs={'class':'form-control', 'placeholder':'Price in dollars'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please enter the information' + 
    ' about the condition of the book. For instance: Book is on pretty good condition.', 'row':'5'}))

    class Meta:
        model= Sell_book
        fields = ['book_title',
                  'isbn_no',
                  'author',
                  'price',
                  'negotiable',
                  'description',
                  'photo']


