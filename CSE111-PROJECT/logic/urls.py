from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name="home"),
    path('create-poll/', views.create_poll, name="create-poll"),
    path('delete-poll/<str:pk>/', views.delete_poll, name="delete-poll"),
    path('delete-comment/<str:pk>/', views.delete_comment, name="delete-comment"),
    path('create_topic/', views.create_topic, name='create_topic'),
    path('comment/<str:pk>/', views.comment, name="comment"),
    path('all-topics', views.alltopics, name="all-topics"),
    path('user-Profile/<str:pk>/', views.userProfile, name="user-Profile"),
    path('user-ProfileSavedPost/<str:pk>/', views.savedPosts, name="saved-Post"),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('edit-profile', views.editProfile, name="edit-Profile"),
    path('upvote-poll/<int:poll_id>/', views.upvote_poll, name='upvote_poll'),
    path('downvote-poll/<int:poll_id>/', views.downvote_poll, name='downvote_poll'),
    path('follow/<int:profile_id>/', views.follow, name='follow'),
    path('unfollow/<int:profile_id>/', views.unfollow, name='unfollow'),
    path('followlist/<int:profile_id>/', views.followlist, name='followlist'),
    path('unfollowlist/<int:profile_id>/', views.unfollowlist, name='unfollowlist'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('toggle-save-post/<int:poll_id>/', views.toggle_save_post, name='toggle-save-post'),

]
