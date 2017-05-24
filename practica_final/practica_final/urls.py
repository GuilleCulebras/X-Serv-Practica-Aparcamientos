"""practica_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from aparcamientos import views
from django.views.static import serve
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.pagina_principal, name = 'Pagina principal'),
    url(r'^login', views.logIN),
    url(r'^logout', logout, {'next_page' : '/'}),
    url(r'^cambiartitulo$', views.cambiarTitulo),
    url(r'^mypage', views.myPage),
    url(r'^aparcamientos$', views.allParkings),
    url(r'^aparcamientos/(.+)$', views.parkingId),
    url(r'^filtparking$', views.filtParking),
    url(r'^addselected/(.+)$',views.addSelected),
    url(r'^addcomment/(.+)$',views.addComment),
    url(r'^main/xml$', views.mainXml),
    url(r'^(.*)/xml$', views.userXml),
    url(r'^about/$',views.aboutPage),
    url(r'^rsschannel$', views.rssChannel),
    url(r'^register$',views.register),
    url(r'^(.*)$',views.usuario),

]
