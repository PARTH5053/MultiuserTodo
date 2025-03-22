
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.signup,name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/',views.home,name='home'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('logout/',views.logout_view,name='logout'),
]
