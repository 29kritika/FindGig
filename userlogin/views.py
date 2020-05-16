from django.db.models import Q
from django.shortcuts import render, redirect
from .models import User, Event, Post
from .forms import CustomUserCreationForm, Bio, Name, City, Gender, EventCreationForm, PostCreationForm
from django.http import Http404
from django.views.generic import CreateView
from embed_video.backends import detect_backend


# _______________________Classes__________________________


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
    if user.type == 'artist':
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
        return render(request, 'ip/dashboard.html', args)
    if user.type == 'band':
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
        return render(request, 'ip/dashboard_band.html', args)
    # Find the events organised by this user
    # send it to the html page in order to display his events temporarily
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
        #print(events)
        args['events'] = events
        return render(request, 'ip/dashboard_org.html', args)
    except:
        print('something')
        pass
    return render(request, 'ip/dashboard_org.html', args)


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
        return render(request, 'ip/profile_org.html', args)

    posts = Post.objects.all().filter(performer=puser)
    args['posts'] = posts
    args['pusersid']=id
    return render(request, 'ip/profile.html', args)

def sponsor(request, eventid):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    event = Event.objects.get(id=eventid)
    event.sponsor = user
    event.save()
    return redirect('Home')

def asettings(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    checkArtist(user)
    return render(request, 'artists/asettings.html')


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
    # socialuser = request.user
    # user = User.objects.get(user=socialuser)
    # will be editable for organiser (need to add that)

    event = Event.objects.get(id=id)
    args = {'event': event}
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

    return render(request, 'ip/searchresult.html', args)
    # return render(request, 'artists/search-bands.html', {'search_set': list(set(queryset))})


# def search_artists():
#     pass
#
#
# def search_events():
#     pass
#
#
# def search_organisers():
#     pass


def allEvents(request):
    pass


