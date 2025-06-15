from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.post_list, name='post-list'),
    path('category/<slug:slug>/', views.category_posts, name='category-posts'),
    path('users/', views.user_list, name='user-list'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('contact/', views.contact_view, name='contact'),
    path('search/', views.search_posts, name='search_posts'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),

    #path('post/<int:post_id>/<slug>/', views.post_detail, name='post_detail')
    path('post/<int:post_id>/<slug:post_slug>/', views.post_detail, name='post_detail'),

    path('post/<int:post_id>/<slug:post_slug>/', views.post_detail, name='post-detail'),
    #path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('support/', views.support_view, name='support'),
    path('quiz/', views.quiz_home, name='quiz_home'),
    path('quiz/start/', views.random_quiz, name='random_quiz'),
    path('quiz/start/<int:category_id>/', views.random_quiz, name='quiz_by_category'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/', views.quiz_view, name='quiz'),
    #path('quiz/', include('stemverse.urls')), 
]

  





