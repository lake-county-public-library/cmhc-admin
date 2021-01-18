from django import forms

class CsvForm(forms.Form):
  csv_filename = forms.CharField(label='', initial='cmhc.csv', max_length=100)
