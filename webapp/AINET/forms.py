from django.forms import ModelForm
from django import forms
from .models import Client, Site, Zone, Camera
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
 
class AddCameraForm(ModelForm):
    class Meta:
        model = Camera
        fields = ['number', 'ref', 'maker', 'resolution', 'IP', 'port', 'zone']
        widgets = {
            'zone': forms.Select(attrs={'class': 'select-field'}),
            'number': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'ref': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'maker': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'resolution': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'IP': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'port': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
        }


class AddSiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'address', 'country', 'state_province', 'city', 'country']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'address': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'country': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'state_province': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'city': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'country': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
        }        

class AddZoneForm(ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'site']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'name': 'field1',
            }),
            'zone': forms.Select(attrs={'class': 'select-field'}),
            
        }                