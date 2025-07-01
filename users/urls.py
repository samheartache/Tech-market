from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.UserRegister.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('account/', views.UserAccount.as_view(), name='account'),
    path('logout/', views.logout, name='logout'),
    path('editprofile/', views.UserEdit.as_view(), name='editprofile'),
    path('sendreview/', views.SendReviewView.as_view(), name='sendreview')
]