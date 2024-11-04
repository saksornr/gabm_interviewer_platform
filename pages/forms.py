from django import forms
from allauth.account.forms import SignupForm

from .interview_settings import *

class ConsentForm(forms.Form):
  first_name = forms.CharField(label='Enter your first name')
  last_name = forms.CharField(label='Enter your last name')


class SpriteSheetForm(forms.Form):
  front = forms.ImageField()
  spritesheet = forms.ImageField()
  right_gif = forms.FileField()
  back_gif = forms.FileField()
  left_gif = forms.FileField()
  front_gif = forms.FileField()


class CustomSignupForm(SignupForm):
  def __init__(self, *args, **kwargs):
    super(CustomSignupForm, self).__init__(*args, **kwargs)
    self.fields['username'].required = False
    self.fields['username'].widget = forms.HiddenInput()


  def clean_username(self):
    return 'temporary_username'


  def save(self, request):
    user = super(CustomSignupForm, self).save(request)
    username = self.cleaned_data['email']
    user.username = username
    user.save()
    return user


  def is_valid(self):
    valid = super(CustomSignupForm, self).is_valid()
    print("Form valid:", valid)
    return valid


class SurveyCompletionForm(forms.Form):
  survey_code_pt1 = forms.CharField(label='Enter the completion code from "Survey Part 1":', 
    error_messages={
            'required': 'This field is required.',
            'invalid': 'Enter a valid value.'
        })
  survey_code_pt2 = forms.CharField(label='Enter the completion code from "Survey Part 2":', 
    error_messages={
            'required': 'This field is required.',
            'invalid': 'Enter a valid value.'
        })
  survey_part = forms.CharField(widget=forms.HiddenInput(), initial='1')


  def clean_survey_code(self):
    survey_code = self.cleaned_data['survey_code']
    # Your validation logic here
    if (survey_code != first_survey_code 
      and survey_code != second_survey_code):
      raise forms.ValidationError(f'Enter a valid survey code (it starts with {first_survey_code[:3]}).')
    return survey_code


class ExperimentCodeForm(forms.Form):
  code = forms.CharField(label='Enter the code')



































