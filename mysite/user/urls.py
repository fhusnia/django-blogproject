from django.urls import path
from . import views

app_name='user'

urlpatterns = [
    path('login/',views.login_view,name='login'), # type: ignore
    path('register/',views.register_view,name='register'), # type: ignore
    path('logout/',views.logout_view,name='logout') # type: ignore
]
