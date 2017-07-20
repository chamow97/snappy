from django.conf.urls import url

from twitter_snaps import views

app_name='twitter_snaps'

urlpatterns = [
    url(r'^$', views.index, name='base'),
    url(r'register', views.UserFormView.as_view(), name='register')
]