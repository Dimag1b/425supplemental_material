from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

        url(r'^apps/sevens/admin/', include(admin.site.urls)),
        url(r'^apps/sevens/login/','cleartherack.views.seven_login',name="login"),
        url(r'^apps/sevens/logout/','cleartherack.views.seven_logout',name="logout"),
        url(r'^apps/sevens/app/',include('cleartherack.urls')),
	url(r'^apps/sevens/',include('cleartherack.urls')),
)
