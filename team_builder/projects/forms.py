from django import forms

from . import models


# class ProjectForm(forms.ModelForm):
#     """Build custom form for editing projects beyond standard generic model views"""
#     class Meta:
#         model = models.Project
#         fields = [
#             "name",
#             "owner",
#             # "description",
#             # "timeline",
#             # "requirements",
#         ]


class ProjectForm(forms.ModelForm):
    """Custom form to create new instances of the Project model"""
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'circle--input--h1',
                'placeholder': 'Project Title',
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Project description...',
            }
        )
    )

    timeline = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'circle--textarea--input',
                'placeholder': 'Time estimate',
            }
        )
    )
    requirements = forms.CharField(
        widget=forms.Textarea(
        )
    )

    class Meta:
        model = models.Project
        exclude = ('owner',)
