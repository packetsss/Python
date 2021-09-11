# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from django import forms

class Create_list(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

