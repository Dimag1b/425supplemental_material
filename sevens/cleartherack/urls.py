from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',

        url(r'^dashboard','cleartherack.views.dashboard',name='dashboard'),
        url(r'^leaders','cleartherack.views.leaderboard',name="leaderboard"),
        url(r'^purchase','cleartherack.views.purchase',name="purchase"),
        url(r'^cleartherack','cleartherack.views.cleartherack',name="cleartherack"),
        url(r'^coffee','cleartherack.views.coffeerun',name="coffee"),
        url(r'^Camaraderie','cleartherack.views.ComTrip',name="comtrip"),
        url(r'^status','cleartherack.views.status',name="status"),

        url(r'^','cleartherack.views.dashboard',name='lost'),
)