from django.urls import path
from .views import (
    RegisterView, LoginView, TrainCreateView, 
    TrainSearchView, BookingView, UserBookingsView, AnalyticsView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('trains/', TrainCreateView.as_view()),
    path('trains/search/', TrainSearchView.as_view()),
    path('bookings/', BookingView.as_view()),
    path('bookings/my/', UserBookingsView.as_view()),
    path('analytics/top-routes/', AnalyticsView.as_view()),
]