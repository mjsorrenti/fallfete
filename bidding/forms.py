from django import forms

class EmailInvoiceForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        data = self.cleaned_data['email']
        return data