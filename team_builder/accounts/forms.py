from django import forms

from . import models
from .apps import Applicant


class ProfileForm(forms.ModelForm):
    """Form used as the basis for adding data elements to User model"""
    class Meta:
        model = models.Profile
        fields = (
            'full_name',
            'description',
            'avatar',
            # 'url'
        )


class SkillForm(forms.ModelForm):
    """

    Form used as the basis of adding Skills

    https://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html

    """
    class Meta:
        model = models.Skill
        fields = (
            'skill',
        )


#  formset needed to feed into model formset factory
SkillFormSet = forms.modelformset_factory(
    model=models.Skill,
    form=SkillForm,
)


class ApplicantStatusForm(forms.ModelForm):

    class Meta:
        model = Applicant
        exclude = ('position', 'applicant', 'status', 'project')