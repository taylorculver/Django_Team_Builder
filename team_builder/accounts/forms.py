from django import forms


from . import models
from .apps import Project, Position, Applicant


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = (
            'full_name',
            'description',
            'avatar',
            # 'url'
        )


# Skills Form
class SkillForm(forms.ModelForm):
    skill = forms.CharField(max_length=200)

    class Meta:
        model = models.Skill
        fields = (
            'skill',
        )


#  formset needed to feed into formset factory
SkillFormSet = forms.modelformset_factory(
    model=models.Skill,
    form=SkillForm,
    # fields='__all__'
    # extra=3
)

# formset factory needed to process multiple Position objects per Project object
# SkillsInlineFormSet = forms.inlineformset_factory(
#     model=models.Skill,
#     parent_model=models.Profile,
#     can_delete=False,
#     extra=1,
#     fields=('skill',),
#     formset=SkillFormSet
#     )


class ApplicantStatusForm(forms.ModelForm):
    # status = forms.CharField(max_length=200)

    class Meta:
        model = Applicant
        exclude = ('position', 'applicant', 'status', 'project')