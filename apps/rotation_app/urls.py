from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),    
    url(r'^home$', views.index),
    url(r'^add_top$', views.show_add_top),
    url(r'^add_bottom$', views.show_add_bottom),    
    url(r'^create_combo$', views.show_combomaker),        
    url(r'^process_add_top$', views.process_add_top),
    url(r'^process_add_bottom$', views.process_add_bottom),
    url(r'^edit_top$', views.edit_top),
    url(r'^logoff$', views.logoff),
]