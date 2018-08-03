from django.views.generic import TemplateView


class Profile(TemplateView):
    template_name = "profiles/profile.html"


class EditProfile(TemplateView):
    template_name = "profiles/profile_edit.html"

