from django import forms

from . import models


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
        fields = ('name', 'description', 'timeline', 'requirements',)


class PositionForm(forms.ModelForm):
    """Custom form to create new instances of the Position Model"""
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'circle--input--h3',
                'placeholder': 'Position Title',
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Position description...',
            }
        )
    )

    class Meta:
        model = models.Position
        fields = ('title', 'description',)


#  formset needed to feed into formset factory
PositionFormSet = forms.modelformset_factory(
    model=models.Position,
    form=PositionForm,
)


class ApplicantStatusForm(forms.ModelForm):
    """Form for User to apply to Position"""
    class Meta:
        model = models.Applicant
        exclude = ('position', 'applicant', 'project', 'status')
