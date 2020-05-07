"""FindGig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    path('home/', views.homePage, name='Home'),
    path('signup/', views.signUp, name='Signup'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    path('artist-settings/', views.asettings, name='artist-settings'),
    path('change-bio/', views.change_bio, name='change-bio'),
    path('change-city/', views.change_city, name='change-city'),
    path('change-gender/', views.change_gender, name='change-gender'),
    path('change-name/', views.change_name, name='change-name'),

    # path('home/search-bands/search-bands.html', views.search_bands, name='search-bands'),
    path('home/search.html', views.search, name='search'),
    path('home/search/method="POST"', views.search, name='search1'),

    path('home/create-event/', views.createEvent, name='create-event'),
    path('events/', views.allEvents, name='event-page'),
    url(r'^events/(?P<id>\d+)', views.eventPage, name='event-desciption'),
    path('', views.index),
]
