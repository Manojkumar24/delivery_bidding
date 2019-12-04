from django.urls import path
from bidding import views

app_name = 'bidding'

urlpatterns = [
    path('home/', views.home, name ='home'),
    path('', views.login_page, name='login'),
    path('register_user/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('user_bid/<int:p_id>/', views.user_bid, name='user_bid'),
    path('bid_list/<int:p_id>/', views.bid_list, name='bid_list'),


]
