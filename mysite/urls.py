"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.cache import cache_page
import mysite.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', mysite.views.index, name='index'),
    url(r'^(?P<i>[0-9]+)/$', mysite.views.index_with_page, name='index_with_page'),
    url(r'^details/(?P<job_id>[0-9]+)/$', cache_page(5 * 60)(mysite.views.details), name='details'),
    url(r'^signup/(?P<email>[0-9A-Za-z_\-@.]+)/$', mysite.views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        mysite.views.activate, name='activate'),
    url(r'^new_task/$', mysite.views.new_task, name='new_task'),
]

