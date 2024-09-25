from django import forms
from .models import Book, Member, Transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'total_stock', 'available_stock']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'total_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'outstanding_debt']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'outstanding_debt': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['member', 'book', 'due_date', 'rent_fee', 'late_fee', 'status']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rent_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'late_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        

class IssueBookForm(forms.ModelForm):
    member = forms.ModelChoiceField(queryset=Member.objects.all(), label="Select Member")
    book = forms.ModelChoiceField(queryset=Book.objects.all(), widget=forms.HiddenInput())  # Hide the book field in the form
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Due Date")


    class Meta:
        model = Transaction
        fields = ['member', 'book', 'due_date']

    def __init__(self, *args, **kwargs):
        super(IssueBookForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Issue Book'))  # Add a submit button with crispy forms
