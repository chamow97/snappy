from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.views import View
from TwitterAPI import TwitterAPI
from twitter_snaps.forms import UserForm





api = TwitterAPI(consumer_key, consumer_secret_key, access_token, secret_access_token)

# @login_required
def twitter_feed(request):
    import tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, secret_access_token)
    api = tweepy.API(auth)
    public_tweets = api.home_timeline()
    tweets = []
    for tweet in public_tweets:
        print(tweet)
        status = tweet.text
        # tweet_date = tweet.relative_created_at
        tweets.append({'status':status})
    return tweets

def index(request):
    tweets = twitter_feed(request)
    return render(request, 'index.html', {'tweets' : tweets})

def twitter_snaps(request):
    return render(request, 'twitter_snaps.html')

def login_user(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login_user.html',
                                  {'error_message' : 'Your account has been disabled!'})
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
    return render(request, 'login_user.html')




class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

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
                    return render(request, 'index.html')

        return render(request, self.template_name, {'form':form})





