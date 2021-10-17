from django.forms import ModelForm

from main.models import Profile, Review


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ("full_name", "photo", "gender", "city")


class ReviewModelForm(ModelForm):
    class Meta:
        model = Review
        fields = ("text", "rating",)