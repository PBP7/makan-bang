from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required(login_url='/auth/login')
def show_main(request):
    context = {
        'npm' : '2306123456',
        'name': 'Pak Bepe',
        'class': 'PBP E'
    }

    return render(request, "main.html", context)

# Create your views here.
