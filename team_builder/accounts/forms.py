from django import forms


from . import models


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = models.User
#         fields = (
#             'first_name',
#             'last_name',
#         )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = (
            'full_name',
            'description',
            'avatar',
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
    models.Skill,
    form=SkillForm,
)

# formset factory needed to process multiple Position objects per Project object
SkillsInlineFormSet = forms.inlineformset_factory(
    model=models.Skill,
    parent_model=models.Profile,
    can_delete=False,
    extra=1,
    fields=('skill',),
    formset=SkillFormSet
    )
