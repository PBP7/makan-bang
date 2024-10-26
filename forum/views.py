from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from forum.models import * 
from forum.forms import NewForumForm, ForumReplyForm

# Create your views here.

@login_required(login_url="authentication:login")
def show_forum(request):
    questions = ForumQuestion.objects.all().order_by("-id")
    context = {"questions": questions}

    return render(request, "main_forum.html", context)

@login_required(login_url="authentication:login")
@csrf_exempt
def create_new_forum(request):
    if request.method == "POST":
        question_form = NewForumForm(request.POST)
        
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('forum:show_forum')
    else:
        question_form = NewForumForm()

    context = {'question': question_form}
    return render(request, "new_forum.html", context)

@login_required(login_url="authentication:login")
@csrf_exempt
@require_POST
def new_forum_ajax(request):
    title = strip_tags(request.POST.get("title"))
    question = strip_tags(request.POST.get("question"))
    topic = request.POST.get("topic")
    user = request.user

    errors = {}
    if not title:
        errors['title'] = ["Title cannot be empty."]
    if not question:
        errors['question'] = ["Discussion cannot be empty."]

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    new_question = ForumQuestion(
        title=title, question=question, topic=topic, user=user
    )
    new_question.save()

    return JsonResponse({
        "message": "Forum created successfully",
        "forum_id": new_question.id,
        "forum_title": new_question.title,
    }, status=201)

def edit_forum(request, id):
    forum = ForumQuestion.objects.get(pk = id)
    form = NewForumForm(request.POST or None, instance=forum)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('forum:view_forum', id=forum.pk)

    context = {'form': form}
    return render(request, "edit_forum.html", context)

def delete_forum(request, id):
    forum = ForumQuestion.objects.get(pk = id)
    forum.delete()

    return HttpResponseRedirect(reverse('forum:show_forum'))

@login_required
def view_forum(request, id):
    try:
        forum = ForumQuestion.objects.get(pk=id)
    except ForumQuestion.DoesNotExist:
        return HttpResponseNotFound('Forum question not found')

    comments = ForumReply.objects.filter(question=forum)  # Fetch all comments related to the forum post
    comment_form = ForumReplyForm()

    if request.method == 'POST':
        comment_form = ForumReplyForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.question = forum  # Associate the comment with the forum question
            new_comment.save()

            forum.replycount += 1
            forum.save()

            return redirect('forum:view_forum', id=forum.pk)  # Reload the page to show the new comment

    context = {
        'forum': forum,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'view_forum.html', context)


def public_forum(request):
    topic = request.GET.get('topic', 'all')  # Get the selected topic from query parameters
    if topic == 'all':
        questions = ForumQuestion.objects.all().order_by("-id")  # Show all forum questions
    else:
        questions = ForumQuestion.objects.filter(topic=topic).order_by("-id")  # Filter questions by topic
    topics = ForumQuestion.objects.values_list('topic', flat=True).distinct()  # Get distinct topics for the dropdown
    return render(request, 'main_forum.html', {'questions': questions, 'topics': topics})

def your_posts(request):
    topic = request.GET.get('topic', 'all')  # Get the selected topic from query parameters
    if topic == 'all':
        questions = ForumQuestion.objects.filter(user=request.user).order_by("-id")  # Show only user's posts
    else:
        questions = ForumQuestion.objects.filter(user=request.user, topic=topic).order_by("-id")  # Filter by topic and user
    topics = ForumQuestion.objects.values_list('topic', flat=True).distinct()  # Get distinct topics
    return render(request, 'main_forum.html', {'questions': questions, 'topics': topics})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(ForumReply, pk=comment_id)
    
    forum_question = comment.question
    comment.delete()
    forum_question.replycount -= 1
    forum_question.save()

    return redirect('forum:view_forum', id=forum_question.pk)