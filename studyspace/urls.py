from django.urls import path
from . import views

urlpatterns = [
  path('', views.studyspace, name='studyspace'),
  path('delete-card/<str:id_video>/', views.delete_card, name='delete_card'),
  path('create-card/', views.create_card, name='create_card'),
  path('card/<str:id_video>/',views.card,name = 'card')
]