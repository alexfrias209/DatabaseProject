from django.shortcuts import render, redirect
from .models import Poll, Topic, Profile, Message, Vote
from .forms import PollForm, TopicForm, profileForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm

@login_required(login_url='login')
def follow(request, profile_id):
    current_profile = request.user.profile
    target_user = get_object_or_404(User, id=profile_id)
    if target_user not in current_profile.following.all():
        current_profile.following.add(target_user)
    return redirect('user-Profile', pk=profile_id)

@login_required(login_url='login')
def unfollow(request, profile_id):
    current_profile = request.user.profile
    target_user = get_object_or_404(User, id=profile_id)
    if target_user in current_profile.following.all():
        current_profile.following.remove(target_user)
    return redirect('user-Profile', pk=profile_id)

@login_required(login_url='login')
def toggle_save_post(request, poll_id):
    user_profile = request.user.profile
    poll = get_object_or_404(Poll, id=poll_id)

    # checking if the post is already saved by the user
    if poll in user_profile.saved_posts.all():
        user_profile.unsave_post(poll)
        is_saved = False
    else:
        user_profile.save_post(poll)
        is_saved = True

    #JsonResponse showing if the post is saved or not
    return JsonResponse({"is_saved": is_saved})

@login_required(login_url='login')
def upvote_poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    user = request.user
    vote, created = Vote.objects.get_or_create(userprofile=user, poll=poll)
    
    if created or vote.vote_status == 2:  # if it's a new vote or the user had previously downvoted
        if not created:
            poll.down_votes -= 1  # remove the previous downvote
        
        vote.vote_status = 1
        vote.save()
        poll.upvote()
        return JsonResponse({"up_votes": poll.up_votes, "down_votes": poll.down_votes})
    else:
        return JsonResponse({"up_votes": poll.up_votes, "down_votes": poll.down_votes})

@login_required(login_url='login')
def downvote_poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    user = request.user
    vote, created = Vote.objects.get_or_create(userprofile=user, poll=poll)

    if created or vote.vote_status == 1:  # if it's a new vote or the user had previously upvoted
        if not created:
            poll.up_votes -= 1  # remove the previous upvote
        
        vote.vote_status = 2
        vote.save()
        poll.downvote()
        return JsonResponse({"down_votes": poll.down_votes, "up_votes": poll.up_votes})
    else:
        return JsonResponse({"up_votes": poll.up_votes, "down_votes": poll.down_votes})

def userProfile(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.profile
    poll = user.poll_set.all()  # Polls created by the user
    saved_polls = profile.saved_posts.all()  # polls saved by the user's profile
    topic = Topic.objects.all()
    comments = user.message_set.all()
    poll_full_count = Poll.objects.count()
    context = {
        'user': user,
        'poll': poll,
        'saved_polls': saved_polls,
        'topic': topic,
        'comments': comments,
        'poll_full_count': poll_full_count
    }
    return render(request, 'logic/profile.html', context)


def savedPosts(request, pk):
    user = User.objects.get(pk=pk)
    profile = user.profile
    poll = user.poll_set.all()  # polls created by the user
    saved_polls = profile.saved_posts.all()  # polls saved by the user's profile
    topic = Topic.objects.all()
    comments = user.message_set.all()
    poll_full_count = Poll.objects.count()
    context = {
        'user': user,
        'poll': poll,
        'saved_polls': saved_polls,
        'topic': topic,
        'comments': comments,
        'poll_full_count': poll_full_count
    }
    return render(request, 'logic/saved.html', context)


def validate_unique_topic_name(value):
    if Topic.objects.filter(name__iexact=value).exists():
        raise ValidationError('A topic with that name already exists.')

@login_required(login_url='login')
def followlist(request, profile_id):
    target_user = get_object_or_404(User, id=profile_id)
    target_profile = target_user.profile
    obj = target_profile.following_users()
    blah = "following"
    context = {
        'target_user': target_user,
        'obj': obj,
        'blah':blah
    }
    return render(request, 'logic/friends.html', context)

@login_required(login_url='login')
def unfollowlist(request, profile_id):
    target_user = get_object_or_404(User, id=profile_id)
    target_profile = target_user.profile
    obj = target_profile.followers()
    blah = "followers"
    context = {
        'target_user': target_user,
        'obj': obj,
        'blah':blah
    }
    return render(request, 'logic/friends.html', context)

# def create_topic(request):
#     if request.method == 'POST':
#         request.session['original_referer'] = request.META.get('HTTP_REFERER', '/')
#         form = TopicForm(request.POST)
#         name = request.POST.get('name', '').lower()
#         try:
#             validate_unique_topic_name(name)
#             if form.is_valid():
#                 form.save()
#                 return redirect('home')
#         except ValidationError as e:
#             form.add_error('name', e)
#     else:
#         form = TopicForm()
#     return render(request, 'logic/creation.html', {'form': form})

def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        name = request.POST.get('name', '').lower()
        try:
            validate_unique_topic_name(name)
            if form.is_valid():
                form.save()
                return redirect('home')
        except ValidationError as e:
            form.add_error('name', e)
    else:
        # set the original_referer in the session only on the initial GET request
        request.session['original_referer'] = request.META.get('HTTP_REFERER', '/')
        form = TopicForm()

    return render(request, 'logic/creation.html', {'form': form})

def loginPage(request):
    page = 'login'
    form = CustomUserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            pass
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
    context = {'page':page, 'form':form}
    return render(request, 'logic/login_register.html',context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    def validate_unique_username(value):
        if User.objects.filter(username__iexact=value).exists():
            raise ValidationError('A user with that username already exists.')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        username = request.POST.get('username', '').lower()
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        try:
            validate_unique_username(username)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = username
                user.first_name = first_name  
                user.last_name = last_name 
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error has occured during registration')
        except ValidationError as e:
            messages.error(request, e.message)
    return render(request, 'logic/login_register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    uProfile = Profile.objects.get(user=request.user)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    poll_full_count = Poll.objects.count()
    if q.startswith('@'):
        # search only by username
        username = q[1:]  # remove '@' symbol
        users = User.objects.filter(username__icontains=username)
        poll = Poll.objects.filter(host__in=users)
    else:
        # search by topic_names and debate_titles
        poll = Poll.objects.filter(
            Q(topic__name__icontains=q) | 
            Q(debate_title__icontains=q)
        )
    poll_count = poll.count()
    topic = Topic.objects.annotate(poll_count=Count('poll')).order_by('-poll_count')[:8]
    followed_users = uProfile.following.all()
    users_to_include = followed_users | User.objects.filter(id=request.user.id)
    comments = Message.objects.filter(user__in=users_to_include)
    context = {'uProfile': uProfile, 'poll': poll, 'topic': topic, 'poll_count': poll_count, 'poll_full_count':poll_full_count, 'comments':comments}
    return render(request, 'logic/home.html', context)


@login_required(login_url='login')
def create_poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST, request.FILES)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.host = request.user
            poll.save()
            return redirect('home')
    else:
        # set the original_referer in the session only on the initial GET request
        request.session['original_referer'] = request.META.get('HTTP_REFERER', '/')
        form = PollForm()

    context = {'form': form, 'original_referer': request.session.get('original_referer', '/')}
    return render(request, 'logic/creation.html', context)

@login_required(login_url='login')
def delete_poll(request, pk):
    poll = Poll.objects.get(id=pk)
    mess = poll.debate_title
    if request.method == 'POST':
        poll.delete()
        return redirect ('home')
    context = {'mess': mess}
    return render(request, "logic/delete.html", context)

@login_required(login_url='login')
def comment(request, pk):
    poll = Poll.objects.get(id=pk)
    comments = poll.message_set.all() #Quering child objects of poll. Message is the child. (make sure it's lower case)
    
    if request.method == 'POST':
        comm = Message.objects.create(
            user = request.user,
            post = poll,
            body = request.POST.get('body'),
        )
        return redirect('comment', pk=poll.id)

    context = {'poll': poll,'comments':comments}
    return render(request, "logic/comment_section.html", context)


@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Message.objects.get(id=pk)
    mess = comment.body
    poll_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect('comment', pk=poll_id)
    context = {'mess':mess}
    return render(request, "logic/delete.html", context)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = profileForm(request.POST, request.FILES, instance=profile)  # add request.files
        if form.is_valid():
            form.save()
            return redirect('user-Profile', pk=request.user.id) 
    else:
        form = profileForm(instance=profile)
    context = {'form': form}
    return render(request, "logic/edit-Profile.html", context)


@login_required(login_url='login')
def alltopics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q).order_by('name')
    return render(request, "logic/all-topics.html", {'topics': topics})

@login_required
def delete_user(request):
    user = request.user
    mess = user.username
    context = {'mess': mess}
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('login')  

    return render(request, 'logic/delete.html', context)  