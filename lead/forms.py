from django import forms
from django.forms import ModelForm
from .models import Lead , Agent
from django.contrib.auth.forms import UserCreationForm , UsernameField
from django.contrib.auth import get_user_model



User = get_user_model()

class CreateForm(forms.Form):
  first_name = forms.CharField(max_length=20)
  last_name = forms.CharField(max_length=20)
  age = forms.IntegerField(min_value=0)


class CreateFormModel(ModelForm):
  class Meta:
    model = Lead
    fields = ['first_name',
    'last_name', 'age',
    'agent', 'description',
    'phone_number','email'
    ]


class CustomUserCreationForm(UserCreationForm):
  class Meta:
      model = User
      fields = ("username",)
      field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
  agent = forms.ModelChoiceField(queryset=Agent.objects.none())

  def __init__(self,*args, **kwargs):
    request = kwargs.pop('request')
    agents = Agent.objects.filter(organisation=request.user.userprofile)
    self.fields['agent'].queryset = agents
    super(AssignAgentForm, self).__init__(*args, **kwargs)


class LeadCategoryUpdateForm(forms.ModelForm):
  class Meta:
    model = Lead
    fields = ['category']
