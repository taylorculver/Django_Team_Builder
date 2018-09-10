from django import forms

from . import models
from .apps import Applicant


class ProfileForm(forms.ModelForm):
    """Form used as the basis for adding data elements to User model"""
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter Your Full Name Here',
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell us a little about yourself',
            }
        )
    )

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
    skill = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Skill',
            }
        )
    )

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


class GitHubForm(forms.ModelForm):
    """Form to add GitHub projects to profile"""
    github_project = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Project Name',
            }
        )
    )

    github_url = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Project URL',
            }
        )
    )

    class Meta:
        model = models.GitHub
        fields = (
            'github_project',
            'github_url',
        )


#  formset needed to feed into model formset factory
GitHubFormSet = forms.modelformset_factory(
    model=models.GitHub,
    form=GitHubForm,
)


class ApplicantStatusForm(forms.ModelForm):

    class Meta:
        model = Applicant
        exclude = ('position', 'applicant', 'status', 'project')