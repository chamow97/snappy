from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from twitter_snaps.forms import UserForm
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import tweepy
from django.views.generic import View
import datetime
import threading
from threading import Thread
import nude
from nude import Nude
import urllib.request


def is_nsfw(request, url):
    urllib.request.urlretrieve(
        url, "test.jpg")
    return nude.is_nude('test.jpg')

# authentication for tweepy
from twitter_snaps.models import user_search

consumer_key = 'edvGYBKwCf5LzHVVY3IvVJgmM'
consumer_secret_key = 'X5uKW5wiAbCW9pjqe0ublMBJ5O2PYUeeWqeUbkr17TQNP0KYrL'
access_token = '342784431-eKqhjwlXEBHwcLP8sOxAdl8JjMYiroZs7mcwGBip'
secret_access_token = 'pnYADssIJrlafbH1hH2PgpkKoK5YotBcKkmt30dyLcY2X'


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


def twitter_feed(request, search):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, secret_access_token)
    api = tweepy.API(auth)
    tweets = []
    images = []
    user = []
    for tweet in tweepy.Cursor(api.search,
                               q=str(search + " -filter:retweets"),
                               lang="en",
                               count=10,
                               include_entities=True).items(150):
        if 'media' in tweet.entities:
            for image in tweet.entities['media']:
                img_data = requests.get(image['media_url']).content
                with open('image_name.jpg', 'wb') as handler:
                    handler.write(img_data)
                images.append(image['media_url'])
                tweets.append(tweet.text)
                user.append(tweet.user.name)
    ans_list = [images, tweets, user]
    return ans_list


def tumblr_tags(request, search):
    api_key = 'IRb0id61fySh2utB0nCBPjJZIDgnBUfvTCigcbGRBRgSBrC6Dd'
    url = "https://api.tumblr.com/v2/tagged?tag=" + search + "&api_key=" + api_key
    data = requests.get(url)
    feeds = data.json()
    images = []
    slug = []
    blog = []
    for data in feeds["response"]:
        try:
            for image_data in data["photos"]:
                images.append(image_data["original_size"]["url"])
            slug.append(data["slug"])
            blog.append(data["blog_name"])

        except:
            print("")

    ans_list = [images, slug, blog]
    return ans_list


@csrf_exempt
def searchTags(request):
    search = request.POST.get("search")
    selected_platform = int(request.POST.get("selectedPlatform"))
    if selected_platform == 0:
        search = "#" + search
        tweets = twitter_feed(request, search)
        ans = json.dumps({
            'images': tweets[0],
            'text': tweets[1],
            'user': tweets[2]
        })
        return HttpResponse(ans)
    elif selected_platform == 1:
        tumblr = tumblr_tags(request, search)
        ans = json.dumps({
            'images': tumblr[0],
            'text': tumblr[1],
            'user': tumblr[2]
        })
        return HttpResponse(ans)
    else:
        first_thread = ThreadWithReturnValue(target=twitter_feed, args=(request, "#" + search))
        second_thread = ThreadWithReturnValue(target=tumblr_tags, args=(request, search))
        first_thread.start()
        second_thread.start()
        tweets = first_thread.join()
        tumblr = second_thread.join()
        tweets[0].extend(tumblr[0])
        tweets[1].extend(tumblr[1])
        tweets[2].extend(tumblr[2])
        ans = json.dumps({
            'images': tweets[0],
            'text': tweets[1],
            'user': tweets[2]
        })
        return HttpResponse(ans)


@csrf_exempt
def saveTerms(request):
    search = request.POST.get("search")
    selected_platform = int(request.POST.get("selectedPlatform"))
    current_date_time = datetime.datetime.now()
    try:
        term = user_search.objects.get(search_term=search, user_name=request.user.username, platform=selected_platform)
    except:
        term = user_search(search_term=search, platform=selected_platform, time=current_date_time,
                           user_name=request.user.username)
        term.save()
    return HttpResponse()


def index(request):
    return render(request, 'index.html')


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'login_user.html',
                                  {'error_message': 'Your account has been disabled!'})
            else:
                return render(request, 'login_user.html',
                              {'error_message': 'Incorrect Username / Password!'})

    return render(request, 'login_user.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        'form': form
    }
    return redirect('/')


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')

        return render(request, self.template_name, {'form': form})
