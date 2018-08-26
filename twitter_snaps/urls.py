from django.conf.urls import url

from twitter_snaps import views

app_name='twitter_snaps'

urlpatterns = [
    url(r'^$', views.index, name='base'),
    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user$', views.login_user, name='login_user'),
    url(r'^logout_user$', views.logout_user, name='logout_user'),
    url(r'^searchTags$', views.searchTags, name='searchTags'),
    url(r'^saveTerms$', views.saveTerms, name='saveTerms')
]