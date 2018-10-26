from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),    
    url(r'^home$', views.index),
    url(r'^get_lucky$', views.random_combo),            
    url(r'^create_combo$', views.show_combomaker),        
    url(r'^process_combo$', views.process_combo),    
    url(r'^browse_combos$', views.show_combobrowser),    
    url(r'^delete_combo$', views.delete_combo),        
    url(r'^schedule_combo$', views.show_comboscheduler),        
    url(r'^delete_scheduled$', views.delete_scheduled_combo),    
    url(r'^show_schedule$', views.show_schedule),    
    url(r'^process_schedulecombo$', views.process_schedulecombo),
    url(r'^tops$', views.tops),
    url(r'^add_top$', views.show_add_top),
    url(r'^process_add_top$', views.process_add_top),
    url(r'^edit_top/(?P<id>[0-9]+)$', views.edit_top),
    url(r'^process_edit_top/(?P<id>[0-9]+)$', views.process_edit_top),
    url(r'^delete_top/(?P<id>[0-9]+)$', views.delete_top),
    url(r'^bottoms$', views.bottoms),
    url(r'^add_bottom$', views.show_add_bottom),    
    url(r'^process_add_bottom$', views.process_add_bottom),
    url(r'^edit_bottom/(?P<id>[0-9]+)$', views.edit_bottom),
    url(r'^process_edit_bottom/(?P<id>[0-9]+)$', views.process_edit_bottom),
    url(r'^delete_bottom/(?P<id>[0-9]+)$', views.delete_bottom),
    url(r'^logoff$', views.logoff),

]