from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),
    path('editprofile/', views.editprofile, name='editprofile')
]