
from ecomm import settings
from django.urls import path
from django.conf.urls.static import static 
from ecomm_app import views

urlpatterns = [
   # path('about',views.about),
    path('contact',views.contact),
    path('home',views.home),
    path('edit/<sid>',views.edit_fun),
    path('delete/<sid>',views.delete),
    path("GetData",views.SimpleView.as_view()),
    path('hello',views.hello),
    path('pdetails/<pid>',views.product_details),
    path('viewcart',views.viewcart),
    path('register',views.user_register,name='register'),
    path('login',views.user_login, name='login'),
    path('logout',views.user_logout),
    path('catfilter/<cv>', views.catfilter),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment),
    
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)