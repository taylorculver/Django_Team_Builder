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

# Project Form
