from django.shortcuts import render,redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from preference.forms import PreferenceForm
from preference.models import Preference
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


# Create your views here.
@login_required
def show_preference(request):
    preference_entries = Preference.objects.filter(user=request.user)  
    context = {
        'preference_entries': preference_entries
    }
    return render(request, "add_preference.html", context)


@login_required
@csrf_exempt
@require_POST
def add_preference_ajax(request):
    if request.method == "POST":
        preference_name = strip_tags(request.POST.get("preference_name"))
        user = request.user

        # Check for a valid preference name
        if preference_name:
            # Create and save the new preference
            new_preference = Preference(preference=preference_name, user=user)
            new_preference.save()

            # Return a JSON response
            return JsonResponse({"status": "success", "id": new_preference.id}, status=201)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
@require_http_methods(["DELETE"])
def delete_preference_ajax(request, preference_id):
    try:
        # Make sure the preference belongs to the logged-in user
        preference = Preference.objects.get(id=preference_id, user=request.user)
        preference.delete()
        return JsonResponse({"status": "success"}, status=200)
    except Preference.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Preference not found"}, status=404)
