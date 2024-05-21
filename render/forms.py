from django import forms

class UUIDForm(forms.Form):
    uuid = forms.UUIDField(label="UUIDを入力してください", required=True)
    