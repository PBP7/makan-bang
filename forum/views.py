import json
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
    topic = request.GET.get('topic', 'All Topic')
    if topic == 'All Topic':
        questions = ForumQuestion.objects.all().order_by("-id")
    else:
        questions = ForumQuestion.objects.filter(topic=topic).order_by("-id")
    
    context = {
        "questions": questions,
        "current_topic": topic
    }
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
    topic = request.GET.get('topic', 'All')  # Get the selected topic from query parameters
    if topic == 'All':
        questions = ForumQuestion.objects.all().order_by("-id")  # Show all forum questions
    else:
        questions = ForumQuestion.objects.filter(topic=topic).order_by("-id")  # Filter questions by topic
    topics = ForumQuestion.objects.values_list('topic', flat=True).distinct()  # Get distinct topics for the dropdown
    return render(request, 'main_forum.html', {'questions': questions, 'topics': topics})

def your_posts(request):
    topic = request.GET.get('topic', 'All')  # Get the selected topic from query parameters
    if topic == 'All':
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

def get_questions_json(request):
    topic = request.GET.get('topic', 'All Topic')
    
    try:
        if topic == 'All Topic':
            questions = ForumQuestion.objects.all().order_by("-id")
        else:
            questions = ForumQuestion.objects.filter(topic=topic).order_by("-id")
        
        questions_data = []
        for question in questions:
            question_dict = {
                'id': question.id,
                'title': question.title,
                'question': question.question,
                'topic': question.topic,
                'replycount': question.replycount,
                'created_at': question.created_at.isoformat(),
                'user': {
                    'id': question.user.id,
                    'username': question.user.username,
                },
                'replies': [{
                    'id': reply.id,
                    'reply': reply.reply,
                    'created_at': reply.created_at.isoformat(),
                    'user': {
                        'id': reply.user.id,
                        'username': reply.user.username,
                    }
                } for reply in question.replies.all()]
            }
            questions_data.append(question_dict)
        
        return JsonResponse(questions_data, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
def get_replies_json(request, question_id):
    try:
        question = get_object_or_404(ForumQuestion, pk=question_id)
        
        replies = ForumReply.objects.filter(question=question).order_by("-created_at")
        
        replies_data = []
        for reply in replies:
            reply_dict = {
                'id': reply.id,
                'reply': reply.reply,
                'created_at': reply.created_at.isoformat(),
                'user': {
                    'id': reply.user.id,
                    'username': reply.user.username,
                },
                'question': {
                    'id': reply.question.id,
                    'title': reply.question.title
                }
            }
            replies_data.append(reply_dict)
        
        return JsonResponse(replies_data, safe=False)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
@csrf_exempt
def create_forum_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            new_forum = ForumQuestion.objects.create(
                title=data['title'],
                question=data['question'],
                topic=data['topic'],
                user=request.user,
                replycount=0
            )
            
            forum_data = {
                'id': new_forum.id,
                'title': new_forum.title,
                'question': new_forum.question,
                'topic': new_forum.topic,
                'replycount': new_forum.replycount,
                'created_at': new_forum.created_at.isoformat(),
                'user': {
                    'id': new_forum.user.id,
                    'username': new_forum.user.username,
                },
                'replies': []
            }
            
            return JsonResponse({
                "status": "success",
                "message": "Forum created successfully",
                "forum": forum_data
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

@csrf_exempt
def edit_forum_flutter(request, id):
    if request.method == 'POST':
        try:
            forum = ForumQuestion.objects.get(pk=id)
            data = json.loads(request.body)
            
            if forum.user != request.user and request.user.username.lower() != 'admin':
                return JsonResponse({
                    "status": "error",
                    "message": "You don't have permission to edit this forum"
                }, status=403)
            
            forum.title = data['title']
            forum.question = data['question']
            forum.topic = data['topic']
            forum.save()
            
            forum_data = {
                'id': forum.id,
                'title': forum.title,
                'question': forum.question,
                'topic': forum.topic,
                'replycount': forum.replycount,
                'created_at': forum.created_at.isoformat(),
                'user': {
                    'id': forum.user.id,
                    'username': forum.user.username,
                },
                'replies': [{
                    'id': reply.id,
                    'reply': reply.reply,
                    'created_at': reply.created_at.isoformat(),
                    'user': {
                        'id': reply.user.id,
                        'username': reply.user.username,
                    }
                } for reply in forum.replies.all()]
            }
            
            return JsonResponse({
                "status": "success",
                "message": "Forum updated successfully",
                "forum": forum_data
            })
        except ForumQuestion.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Forum not found"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

@csrf_exempt
def delete_forum_flutter(request, id):
    if request.method == 'POST':
        try:
            forum = ForumQuestion.objects.get(pk=id)
            
            if forum.user != request.user and request.user.username.lower() != 'admin':
                return JsonResponse({
                    "status": "error",
                    "message": "You don't have permission to delete this forum"
                }, status=403)
            
            forum.delete()
            return JsonResponse({
                "status": "success",
                "message": "Forum deleted successfully"
            })
        except ForumQuestion.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Forum not found"
            }, status=404)
        
@csrf_exempt
def create_reply_flutter(request, forum_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            forum = ForumQuestion.objects.get(pk=forum_id)
            
            new_reply = ForumReply.objects.create(
                reply=data['reply'],
                user=request.user,
                question=forum
            )
            
            forum.replycount += 1
            forum.save()
            
            reply_data = {
                'id': new_reply.id,
                'reply': new_reply.reply,
                'created_at': new_reply.created_at.isoformat(),
                'user': {
                    'id': new_reply.user.id,
                    'username': new_reply.user.username,
                }
            }
            
            return JsonResponse({
                'status': 'success',
                'message': 'Reply added successfully',
                'reply': reply_data
            })
            
        except ForumQuestion.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Forum not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

@csrf_exempt
def delete_reply_flutter(request, reply_id):
    if request.method == 'POST':
        try:
            reply = ForumReply.objects.get(pk=reply_id)
            
            if reply.user != request.user and request.user.username.lower() != 'admin':
                return JsonResponse({
                    "status": "error",
                    "message": "You don't have permission to delete this reply"
                }, status=403)
            
            forum_question = reply.question
            
            reply.delete()
            
            forum_question.replycount -= 1
            forum_question.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Reply deleted successfully"
            })
        except ForumReply.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Reply not found"
            }, status=404)