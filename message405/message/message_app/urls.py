from message_app import views
from django.urls import include, path

urlpatterns = [
    
    path('hello', views.hello),
    path('create', views.create),
    path('dashboard', views.dashboard),
    path('delete/<rid>',views.delete),
    path('edit/<rid>',views.edit),
    
]
