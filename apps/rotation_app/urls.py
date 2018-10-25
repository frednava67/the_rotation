from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),    
    url(r'^home$', views.index),
    url(r'^add_top$', views.show_add_top),
    url(r'^add_bottom$', views.show_add_bottom),    
    url(r'^create_combo$', views.show_combomaker),        
    url(r'^process_combo$', views.process_combo),    
    url(r'^browse_combos$', views.show_combobrowser),    
    url(r'^schedule_combo$', views.show_comboscheduler),        
    url(r'^process_add_top$', views.process_add_top),
    url(r'^process_schedulecombo$', views.process_schedulecombo),
    url(r'^show_schedule$', views.show_schedule),    
    url(r'^process_add_bottom$', views.process_add_bottom),
    url(r'^tops$', views.tops),
    url(r'^bottoms$', views.bottoms),
    url(r'^logoff$', views.logoff),
    url(r'^delete_top/(?P<id>\d+)$', views.delete_top),
    url(r'^delete_bottom/(?P<id>\d+)$', views.delete_bottom),
]