from django.forms import ModelForm
from preference.models import Preference
from django.utils.html import strip_tags

class PreferenceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preference'].widget.attrs.update({
            'class': 'w-full px-2 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#FFCD64] focus:border-transparent resize-y',
            'placeholder': 'Enter your preference here...',
        })

    class Meta:
        model = Preference
        fields = ["preference"]

    def clean_preference(self):
        preference = self.cleaned_data["preference"]
        return strip_tags(preference)