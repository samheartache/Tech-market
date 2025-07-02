from django.urls import path

from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('sendreview/', views.SendReviewView.as_view(), name='sendreview'),
    path('deletereview/', views.DeleteReviewView.as_view(), name='deletereview')
]