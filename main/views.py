from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from preference.models import Preference

# Create your views here.
def show_main(request):
    # Fetch the preferences for the current user
    
    # Pass the preferences along with other context data
    context = {
        'nama': request.user.username,
    }

    return render(request, "main.html", context)
