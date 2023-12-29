# Author: Piotr Cieślak

from django import forms

COMPANIES = (
    ('apple', 'APPLE'),
    ('nvidia', 'NVIDIA'),
    ('amd', 'AMD'),
    ('amazon', 'AMAZON'),
    ('microsoft', 'MICROSOFT'),
)

class ChooseCompanyForm(forms.Form):
    company = forms.ChoiceField(widget=forms.Select(attrs={'onchange': 'submit();'}), choices=COMPANIES, label=False)
