from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Введите имя пользователя'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'Введите email'
            elif field_name == 'password1':
                field.widget.attrs['placeholder'] = 'Введите пароль'
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Подтвердите пароль'


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar', 'first_name', 'last_name', 'linkedin', 'website', 'github')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': ' '}),
        }
