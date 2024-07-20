from django.urls import path
from . import views # This . package just means "the current package; we are importing the sister file "views.py"
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name='home'),
    path('find_bidets/', views.find_bidets, name='find_bidets'),
    path('add_bidet/', views.add_bidet, name='add_bidet'),
    path('bidet/<str:bidet_name>/', views.bidet_detail, name='bidet_detail'),
    path("accounts/login/", views.login_view, name="login_view"),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('guest-login/', views.guest_login, name='guest_login'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    ]

#This is the url patterns that redirect to different pages of our page
#the noteworthy thing here maybe the specific path for the different bidets in line 10, and the reviews in line 15.