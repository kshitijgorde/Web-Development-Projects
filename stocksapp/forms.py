from django import forms

class UploadCSVForm(forms.Form):
    select_type = forms.ChoiceField(choices=[('Company Data', 'company data'),('Stocks Data', 'stocks data')])
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


