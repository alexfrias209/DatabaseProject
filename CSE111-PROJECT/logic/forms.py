from django.forms import ModelForm
from .models import Poll, Topic, Profile
from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ClearableFileInput

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['topic', 'debate_title', 'photo']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']

class CustomClearableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        template = super().render(name, value, attrs, renderer)
        return template.replace('checkbox', 'hidden')

    def is_initial(self, value):
        return False


class profileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'name', 'email', 'bio']
        widgets = {
            'profile_image': CustomClearableFileInput
        }

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name',)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name',)
