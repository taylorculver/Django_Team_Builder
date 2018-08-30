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
        # logged in user is excluded from form but collected during the view
        exclude = ('owner',)


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
        # current project is excluded from form but collected through relationship with project model
        exclude = ('project',)


#  formset needed to feed into formset factory
PositionFormSet = forms.modelformset_factory(
    models.Position,
    form=PositionForm,
)

# formset factory needed to process multiple Position objects per Project object
PositionInlineFormSet = forms.inlineformset_factory(
    model=models.Position,
    parent_model=models.Project,
    can_delete=False,
    extra=1,
    fields=('title', 'description'),
    widgets={
    #     # 'title': forms.Textarea(
    #     #     attrs={'class': 'circle--input--h3', 'placeholder': 'Position Title'}),
        'description': forms.Textarea(
            attrs={'placeholder': 'Position description...'})},
    formset=PositionFormSet
    )


class ApplicationForm(forms.ModelForm):
    # status = forms.CharField(max_length=200)

    class Meta:
        model = models.Application
        exclude = ('position', 'applicant', 'status')
