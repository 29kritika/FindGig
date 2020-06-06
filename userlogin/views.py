import os
import pickle
import pytz
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from google.auth.transport.requests import Request
from .models import *
from .forms import *
from django.http import Http404
from FindGig.settings import STATICFILES_DIRS
from notifications.signals import notify
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime


def create_event(event):
    SCOPES = "https://www.googleapis.com/auth/calendar"
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                STATICFILES_DIRS[0] + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    start_datetime = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
    end_datetime = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
    start_datetime = start_datetime.replace(year=event.date.year, month=event.date.month, day=event.date.day, hour=event.startTime.hour,
                           minute=event.startTime.minute)
    end_datetime = end_datetime.replace(year=event.date.year, month=event.date.month, day=event.date.day, hour=event.endTime.hour,
                         minute=event.endTime.minute)
    body = {
        'summary': event.title,
        'description': event.description,
        'start': {'dateTime': start_datetime.isoformat()},
        'end': {'dateTime': end_datetime.isoformat()},
    }
    cal_event = service.events().insert(calendarId='primary', body=body).execute()
    return cal_event.get('htmlLink')


# ____________________Functions____________________________


def index(request):
    return render(request, 'index.html')


def checkArtistOrBand(user):
    if user.type == 'artist' or user.type == 'band':
        return
    raise Http404('not allowed ')


def checkOrganiser(user):
    if user.type == 'organiser':
        return
    raise Http404('not allowed ')


def get_posts(user, givenposts):
    liked_posts = RatedPost.objects.filter(liked=True, viewer=user)
    disliked_posts = RatedPost.objects.filter(liked=False, viewer=user)
    posts = []
    for post in givenposts:
        if liked_posts.filter(posts=post).count() == 0:
            liked = False
        else:
            liked = True
        if disliked_posts.filter(posts=post).count() == 0:
            disliked = False
        else:
            disliked = True
        posts.append((post, liked, disliked))
    return posts


def homePage(request):
    socialUser = request.user
    try:
        user = User.objects.get(user=socialUser)
    except:
        if type(socialUser) != 'AnonymousUser':
            return redirect('Signup')
    args = {'user': user, }
    posts = Post.objects.all()
    args['posts'] = get_posts(user, posts)
    recommended = related_post(user)
    args['recommended'] = get_posts(user, recommended)
    if user.type == 'artist' or user.type == 'band':
        if request.method == 'POST':
            form = PostCreationForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                Post.objects.update_or_create(
                    performer=user,
                    description=event.description,
                    video=event.video,
                )
                return redirect('Home')
            else:
                print("why dude")
        else:
            form = PostCreationForm()
        args['form'] = form
        return render(request, 'artists/dashboard.html', args)
    if user.type == 'custom user':
        if request.method == 'POST':
            form = PostCreationForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                Post.objects.update_or_create(
                    performer=user,
                    description=event.description,
                    video=event.video,
                )
                return redirect('Home')
        else:
            form = PostCreationForm()
        args['form'] = form
        return render(request, 'custom/dashboard.html', args)
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            link = create_event(event)
            Event.objects.update_or_create(
                organiser=user,
                title=event.title,
                description=event.description,
                venue=event.venue,
                date=event.date,
                startTime=event.startTime,
                endTime=event.endTime,
                video=event.video,
                calendar_link=link
            )
            return redirect('Home')
    else:
        form = EventCreationForm()
    args['form'] = form
    return render(request, 'organisers/dashboard_org.html', args)


def signUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.update_or_create(
                user=request.user,
                type=user.type,
                username=user.username,
                name=user.name
            )
            return redirect('/')
    else:
        form = CustomUserCreationForm
    arg = {'form': form}
    return render(request, 'signup.html', arg)


def profile(request, id):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    args = {'user': user, }
    puser = User.objects.get(id=id)
    args['puser'] = puser
    if puser.type == 'organiser':
        events = Event.objects.all().filter(organiser=puser)
        args['events'] = events
        return render(request, 'organisers/profile_org.html', args)
    if puser.type == 'custom user':
        return render(request, 'custom/profile.html', args)
    posts = Post.objects.all().filter(performer=puser)
    args['posts'] = get_posts(user, posts)
    args['pusersid'] = id
    return render(request, 'artists/profile.html', args)


def view_my_profile(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    return profile(request, user.id)


def new_gigs(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    events = Event.objects.all()
    args = {'user': user, 'events': events}
    return render(request, 'newgigs.html', args)


def sponsor(request, eventid):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    event = Event.objects.get(id=eventid)
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            sponsor = form.save(commit=False)
            Sponsor.objects.update_or_create(
                sponsor=user,
                Amount=sponsor.Amount,
                Event=event,
            )
            verb = user.name + " wishes to sponsor your event " + event.title + "\nAmount: Rs." + str(sponsor.Amount)
            recipient = event.organiser.user
            notify.send(user, recipient=recipient, verb=verb, target=event)
            return redirect('Home')
    else:
        form = SponsorForm
    arg = {'form': form}
    return render(request, 'sponsor.html', arg)


def perform(request, eventid):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    checkArtistOrBand(user)
    event = Event.objects.get(id=eventid)
    Performer.objects.update_or_create(
        performer=user,
        event=event,
        request_accepted=False
    )
    verb = user.name + " wishes to perform at your event " + event.title
    recipient = event.organiser.user
    notify.send(user, recipient=recipient, verb=verb, target=event)
    return redirect('Home')


def change_bio(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = Bio(request.POST)
        if form.is_valid():
            bio = form.save(commit=False)
            user.about_text = bio.about_text
            user.about_link = bio.about_link
            user.save()
            return redirect('Home')
    else:
        form = Bio()
    arg = {'form': form, }
    return render(request, 'change_info.html', arg)


def change_name(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = Name(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            user.name = name.name
            user.save()
            return redirect('Home')
    else:
        form = Name()
    arg = {'form': form, }
    return render(request, 'change_info.html', arg)


def change_city(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = City(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            user.city = city.city
            user.save()
            return redirect('Home')
    else:
        form = City()
    arg = {'form': form, }
    return render(request, 'change_info.html', arg)


def change_gender(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = Gender(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            user.gender = name.gender
            user.save()
            return redirect('Home')
    else:
        form = Gender()
    arg = {'form': form, }
    return render(request, 'change_info.html', arg)


def eventPage(request, id):
    socialuser = request.user
    user = User.objects.get(user=socialuser)
    event = Event.objects.get(id=id)
    sponsors = Sponsor.objects.all().filter(Event=event)
    performers = Performer.objects.all().filter(event=event, request_accepted=True)
    performer_reqs = Performer.objects.all().filter(event=event, responded=False)
    check_sponsor = True
    for s in sponsors:
        if s.sponsor == user:
            check_sponsor = False
            break
    check_performer = True
    for p in performers:
        if p.performer == user:
            check_performer = False
            break
    user_is_org = False
    if event.organiser == user:
        check_sponsor = False
        check_performer = False
        user_is_org = True
    args = {'event': event, 'sponsors': sponsors, 'check_sponsor': check_sponsor, 'check_performer': check_performer,
            'performers': performers, 'user_is_org': user_is_org, 'performer_reqs': performer_reqs, 'user': user}
    return render(request, 'events/AboutEvent.html', args)


def search(request):
    queryset = []
    query = str(request.POST.get("q", ""))
    queries = query.split(" ")
    for q in queries:
        qe = User.objects.all()
        qe = qe.filter(
            Q(username__icontains=q) |
            Q(name__icontains=q) |
            Q(about_text__icontains=q) |
            Q(gender__icontains=q) |
            Q(city__icontains=q)
        ).distinct()
        for qq in qe:
            queryset.append(qq)
    user = User.objects.get(user=request.user)
    args = {'search_set': list(set(queryset)), 'user': user}
    return render(request, 'searchresult.html', args)


def view_notifications(request):
    socialUser = request.user
    list1 = socialUser.notifications.unread()
    list2 = socialUser.notifications.read()
    list1.mark_all_as_read()
    args = {'notifs_read': list2, }
    return render(request, 'notif.html', args)


def acceptPerformer(request, eventId, perfId):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    event = Event.objects.get(id=eventId)
    performer_user = User.objects.get(id=perfId)
    if event.organiser != user:
        raise Http404('You are not authenticated to make changes to this event')
    p = Performer.objects.filter(event=event, performer=performer_user)
    for performer in p:
        performer.request_accepted = True
        performer.responded = True
        performer.save()
        verb = 'Your request to perform at ' + event.title + 'has been accepted'
        notify.send(user, recipient=performer.performer.user, verb=verb, target=event)
    return redirect('view-notifications')


def declinePerformer(request, eventId, perfId):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    event = Event.objects.get(id=eventId)
    performer_user = User.objects.get(id=perfId)
    if event.organiser != user:
        raise Http404('You are not authenticated to make changes to this event')
    p = Performer.objects.filter(event=event, performer=performer_user)
    for performer in p:
        performer.request_accepted = False
        performer.responded = True
        performer.save()
        verb = 'Your request to perform at ' + event.title + 'has been declined'
        notify.send(user, recipient=performer.performer.user, verb=verb, target=event)
    return redirect('view-notifications')


def related_post(user):
    rp = list(RatedPost.objects.all().filter(viewer=user, liked=True).values('posts__description'))
    nl_rp = list(RatedPost.objects.all().filter(viewer=user, liked=False).values('posts__description'))
    queryset = []
    lw = []
    ulw = []
    for i in rp:
        lw.extend(i['posts__description'].split(" "))
    lw = list(set(lw))
    for i in nl_rp:
        ulw.extend(i['posts__description'].split(" "))
    ulw = list(set(ulw))
    for q in lw:
        if q not in ulw:
            qe = Post.objects.all().exclude(performer=user)
            qe = qe.filter(
                Q(description__icontains=q) |
                Q(performer__about_text__icontains=q) |
                Q(performer__name__icontains=q)
            ).distinct()
            for qq in qe:
                queryset.append(qq)
    queryset = list(set(queryset))
    return queryset


def like_post(request, postid):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    post = Post.objects.get(id=postid)
    try:
        query = RatedPost.objects.get(posts=post, viewer=user)
        query.liked = True
        query.save()
    except:
        RatedPost.objects.update_or_create(
            viewer=user,
            liked=True,
            posts=post
        )
    return redirect('Home')


def dislike_post(request, postid):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    post = Post.objects.get(id=postid)
    try:
        query = RatedPost.objects.get(posts=post, viewer=user)
        query.liked = False
        query.save()
    except:
        RatedPost.objects.update_or_create(
            viewer=user,
            liked=False,
            posts=post
        )
    return redirect('Home')
