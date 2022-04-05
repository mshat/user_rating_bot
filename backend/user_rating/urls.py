from django.urls import path
from . import views


urlpatterns = [
    path('users', views.UsersListView.as_view()),
    path('users/<int:tg_user_id>', views.UserView.as_view()),
    path('user_questions', views.UserQuestionsListView.as_view()),
    path('user_answers', views.UserAnswersListView.as_view()),
]