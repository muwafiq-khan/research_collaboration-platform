from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feed/', views.feed_view, name='feed'),
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/collaborate/', views.collaborate_post_view, name='collaborate_post'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('researchers/', views.search_researchers_view, name='search_researchers'),
    path('problems/', views.search_problems_view, name='search_problems'),
    path('problem/<int:problem_id>/', views.problem_detail_view, name='problem_detail'),
    path('project/create/', views.create_project_view, name='create_project'),
    path('project/<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('project/<int:project_id>/collaborate/', views.collaborate_project_view, name='collaborate_project'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('collaboration/<int:request_id>/accept/', views.accept_collaboration_view, name='accept_collaboration'),  # ADD THIS
    path('collaboration/<int:request_id>/reject/', views.reject_collaboration_view, name='reject_collaboration'),  # ADD THIS
]