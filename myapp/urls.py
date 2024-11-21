from django.contrib import admin
from django.urls import path
from myapp import views
from .token import token

urlpatterns = [
    path("", views.index, name="home"),
    path("contact", views.contact, name="contact"),
    path('admin', admin.site.urls),
    path('login', views.loginuser, name="login"),
    path('signup', views.signup, name="Signup"),
    path('forgot', views.forgot, name="Forgot"),
    path('logout',views.loguserout, name="logout"),
    path('resetpass', views.resetpass, name="resetpass"),
    path('reset', views.reset, name="reset"),
    path(f'forgotpass/{token}', views.forgotpass, name="forgotpass"),
    path("account", views.account, name="account"),
    path("deleteuser", views.deleteuser, name="deleteuser"),
    path("changemail", views.changemail, name="changemail")
]