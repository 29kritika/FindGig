import httplib2
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import Http404
from FindGig.settings import STATICFILES_DIRS
from notifications.signals import notify
from django.views.generic import CreateView
from embed_video.backends import detect_backend
from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import http.client
import os
from datetime import timedelta
import datetime
import pytz

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

service_account_email = 'findgig@gogig-274207.iam.gserviceaccount.com'

CLIENT_SECRET_FILE = STATICFILES_DIRS[0] + 'gogig-274207-3c74826599ce.json'

SCOPES = 'https://www.googleapis.com/auth/calendar'
scopes = [SCOPES]


def build_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename=CLIENT_SECRET_FILE, scopes=scopes)

    http = credentials.authorize(httplib2.Http())

    service = build('calendar', 'v3', http=http)

    return service


def create_event(request, args):
    service = build_service()

    start_datetime = datetime.datetime.now(tz=pytz.utc)
    event = service.events().insert(calendarId='primary', body={
        'summary': 'Foo',
        'description': 'Bar',
        'start': {'dateTime': start_datetime.isoformat()},
        'end': {'dateTime': (start_datetime + timedelta(minutes=15)).isoformat()},
        # add attendees
    }).execute()
    print(event)
    return render(request, 'artists/dashboard.html', args)

# ____________________Functions____________________________


def index(request):
    return render(request, 'index.html')


def checkArtist(user):
    if user.type == 'artist':
        return
    raise Http404('not allowed ')


def checkOrganiser(user):
    if user.type == 'organiser':
        return
    raise Http404('not allowed ')


def homePage(request):
    socialUser = request.user
    try:
        user = User.objects.get(user=socialUser)
    except:
        return redirect('Signup')

    args = {'user': user, }
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
        posts = Post.objects.all().filter(performer=user)
        args['posts'] = posts
        events = Event.objects.all()
        args['events'] = events
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
                print("why dude")
        else:
            form = PostCreationForm()
        args['form'] = form
        posts = Post.objects.all().filter(performer=user)
        args['posts'] = posts
        events = Event.objects.all()
        args['events'] = events
        return render(request, 'custom/dashboard.html', args)
    try:
        if request.method == 'POST':
            form = EventCreationForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                Event.objects.update_or_create(
                    organiser=user,
                    title=event.title,
                    description=event.description,
                    venue=event.venue,
                    date=event.date,
                    startTime=event.startTime,
                    endTime=event.endTime,
                    video=event.video,
                )
                return redirect('Home')
            else:
                print("why dude")
        else:
            form = EventCreationForm()
        args['form'] = form
        events = Event.objects.all().filter(organiser=user)
        # print(events)
        args['events'] = events
        return render(request, 'organisers/dashboard_org.html', args)
    except:
        print('something')
        pass
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
            print("why dude")
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

    posts = Post.objects.all().filter(performer=puser)
    args['posts'] = posts
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
    print('events:', events)
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
            return redirect('/')
        else:
            print("why dude")
    else:
        form = SponsorForm
    arg = {'form': form}
    return render(request, 'sponsor.html', arg)


def perform(request, eventid):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
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
            print("why dude")
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
            print("why dude")
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
            print("why dude")
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
            print("why dude")
    else:
        form = Gender()
    arg = {'form': form, }
    return render(request, 'change_info.html', arg)


def createEvent(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    checkOrganiser(user)
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            Event.objects.update_or_create(
                organiser=user,
                title=event.title,
                description=event.description,
                venue=event.venue,
                date=event.date,
                startTime=event.startTime,
                endTime=event.endTime,
                video=event.video,
            )
            return redirect('Home')
        else:
            print("why dude")
    else:
        form = EventCreationForm()
    args = {'form': form, }
    return render(request, 'organisers/createEvent.html', args)


def eventPage(request, id):
    socialuser = request.user
    user = User.objects.get(user=socialuser)
    event = Event.objects.get(id=id)
    sponsors = Sponsor.objects.all().filter(Event=event)
    performers = Performer.objects.all().filter(event=event, request_accepted=True)
    performer_reqs = Performer.objects.all().filter(event=event, responded=False)
    print(performers)
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
    print(performer_reqs)
    for req in performer_reqs:
        print(req.performer.id)
        print(req.event.id)
    args = {'event': event, 'sponsors': sponsors, 'check_sponsor': check_sponsor, 'check_performer': check_performer,
            'performers': performers, 'user_is_org': user_is_org, 'performer_reqs': performer_reqs, 'user':user}
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
            print(qq)
    user = User.objects.get(user=request.user)
    args = {'search_set': list(set(queryset)), 'user': user}
    return render(request, 'searchresult.html', args)


def view_notifications(request):
    socialUser = request.user
    list1 = socialUser.notifications.unread()
    list2 = socialUser.notifications.read()
    list1.mark_all_as_read()
    args = {'notifs_unread': list1, 'notifs_read': list2}
    return render(request, 'notif.html', args)


def acceptPerformer(request, eventId, perfId):
    socialUser = request.user
    event = Event.objects.get(id=eventId)
    print('event;', event)
    performer_user = User.objects.get(id=perfId)
    print('performer_user:', performer_user)
    if event.organiser != user:
        raise Http404('You are not authenticated to make changes to this event')
    print('in accept ')
    p = Performer.objects.filter(event=event, performer=performer_user)
    for performer in p:
        performer.request_accepted = True
        performer.responded = True
        performer.save()

    for perf in p:
        print(perf.event.title)
        print(perf.performer.name)
        print(perf.request_accepted)
    return redirect('view-notifications')


def declinePerformer(request, eventId, perfId):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    event = Event.objects.get(id=eventId)
    performer_user = User.objects.get(id=perfId)
    if event.organiser != user:
        raise Http404('You are not authenticated to make changes to this event')
    performer = Performer.objects.get(event=event, performer=performer_user)
    performer.request_accepted = False
    performer.responded = True
    performer.save()
    return redirect('view-notifications')


def allEvents(request):
    pass
