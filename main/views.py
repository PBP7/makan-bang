from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from preference.models import Preference

# Create your views here.
@login_required(login_url='/auth/login')
def show_main(request):
    # Fetch the preferences for the current user
    preference_entries = Preference.objects.filter(user=request.user)
    
    # Pass the preferences along with other context data
    context = {
        'nama_aplikasi': 'karesu',
        'nama': request.user.username,
        'npm': '2306219575',
        'class': 'PBP B',
        'preference_entries': preference_entries,  # Pass preferences to template
    }

    return render(request, "main.html", context)
