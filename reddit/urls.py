"""django_reddit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.auth.views import password_reset, password_change_done, password_reset_confirm, password_reset_complete, password_reset_done
import views


urlpatterns = [
    url(r'^$', views.frontpage, name="Frontpage"),
    url(r'^j/(?P<subjeffit_title>\w+)/$', views.subjeffit, name="subjeffit"),
    url(r'^comments/(?P<thread_id>[0-9]+)$', views.comments, name="Thread"),
    url(r'^login/$', views.user_login, name="Login"),
    url(r'^logout/$', views.user_logout, name="Logout"),
    url(r'^register/$', views.register, name="Register"),
    url(r'^submit/$', views.submit, name="Submit"),
    url(r'^user/(?P<username>[0-9a-zA-Z_]*)$', views.user_profile, name="User Profile"),
    url(r'^profile/edit/$', views.edit_profile, name="Edit Profile"),
    url(r'^post/comment/$', views.post_comment, name="Post Comment"),
    url(r'^vote/$', views.vote, name="Vote"),
    url(r'^populate/$', views.test_data, name="Create test data"),
    url(r'^accounts/password/reset/$', password_reset, {'template_name': 'public/password_reset.html'}, name="password_reset"),
    url(r'^change-password-done/$', password_reset_done, {'template_name': 'public/password_change_done.html'}, name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'public/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'public/password_reset_complete.html'}, name='password_reset_complete'),
]
