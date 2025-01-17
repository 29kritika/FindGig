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
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import LogoutView

import notifications.urls

urlpatterns = [
    url('', include('social_django.urls', namespace='social')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path('home/', views.homePage, name='Home'),
    path('signup/', views.signUp, name='Signup'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('home/my-profile/', views.view_my_profile, name='view-my-profile'),
    path('home/new-gigs/', views.new_gigs, name='new-gigs'),

    url(r'^home/like-post/(?P<postid>\d+)/$', views.like_post, name='like-post'),
    url(r'^home/dislike-post/(?P<postid>\d+)/$', views.dislike_post, name='dislike-post'),

    path('change-bio/', views.change_bio, name='change-bio'),
    path('change-city/', views.change_city, name='change-city'),
    path('change-gender/', views.change_gender, name='change-gender'),
    path('change-name/', views.change_name, name='change-name'),

    path('home/search.html', views.search, name='search'),
    path('home/search/method="POST"', views.search, name='search1'),
    path('home/notifications/', views.view_notifications, name='view-notifications'),

    path('events/', views.new_gigs, name='event-page'),
    url(r'^events/(?P<id>\d+)/$', views.eventPage, name='event-description'),
    url(r'^events/request-performance/(?P<eventid>\d+)/$', views.perform, name='request-performance'),
    url(r'^events/(?P<eventId>\d+)/accept-performer-request/(?P<perfId>\d+)/$', views.acceptPerformer,
        name='accept-performer-request'),
    url(r'^events/decline-performer-request/(?P<eventId>\d+)/(?P<perfId>\d+)/$', views.declinePerformer,
        name='decline-performer-request'),
    url(r'^view_profile/(?P<id>\d+)/$', views.profile, name='view_profile'),
    url(r'^view_profile/sponsor/(?P<eventid>\d+)/$', views.sponsor, name='sponsor'),
    path('', views.index),
]
