from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Ticket, TicketMessage, Category, Budget


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'id': 'username'
        })
    )


class AdminLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'id': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'password'
        })
    )


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.is_admin = kwargs.pop('is_admin', False)
        super().__init__(*args, **kwargs)
        
        if not self.is_admin:
            # For user forms, exclude category and priority
            self.fields.pop('category')
            self.fields.pop('priority')

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of the problem...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            })
        }


class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message...',
                'id': 'messageText'
            })
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message or not message.strip():
            raise forms.ValidationError("Message cannot be empty")
        return message.strip()


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'assigned_to', 'priority']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show admin users in assigned_to field
        self.fields['assigned_to'].queryset = User.objects.filter(
            userprofile__is_admin=True
        )
        self.fields['assigned_to'].empty_label = "Unassigned"


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'amount', 'spent', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Budget name (e.g., Q1 Hardware Budget)'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'spent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        spent = cleaned_data.get('spent')

        if amount and spent and spent > amount:
            raise forms.ValidationError('Spent amount cannot exceed allocated amount.')

        return cleaned_data