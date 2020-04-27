from django.urls import path
from . import views

app_name = 'rangoapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>', views.category_view, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('goto/', views.goto, name='goto'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('like/', views.like_category, name='like_category'),
    path('suggest/', views.suggest_category, name='suggest_category'),
    path('search_more/', views.search_more_pages, name='search_more'),
    path('profiles/', views.list_profiles, name='profiles'),
    path('auto_add_page/', views.auto_add_page, name='auto_add_page'),

]

