"""locker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from locker import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^LOCKER/(?P<lockerid>\w+)/UPDATE/', views.update_locker_status,name="update_locker_status"),
    url(r'^LOCKER/(?P<lockerid>\w+)/STATUS/', views.get_locker_status,name="get_locker_status"),
    url(r'^TAG/(?P<tagid>\w+)/STATUS/', views.get_tag_status,name="get_tag_status"),
    url(r'^TAG/(?P<tagid>\w+)/REGISTER/', views.register_tag,name="register_tag"),
    url(r'^TAG/(?P<tagid>\w+)/CLEAR/', views.clear_tag,name="clear_tag"),
    url(r'^TAG/(?P<tagid>\w+)/RESERVE/(?P<lockerid>\w+)/(?P<portid>\w+)', views.reserve_locker,name="reserve_locker"),
    url(r'^LOCKER/(?P<lockerid>\w+)/(?P<portid>\w+)/CLEAR/', views.clear_locker,name="clear_locker"),
]
