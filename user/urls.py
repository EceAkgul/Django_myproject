from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    # ex: /home/5/
    path('haber_show/', views.haber_show, name='haber_show'),
    path('haber_ekle/', views.haber_ekle, name='haber_ekle'),
    path('haber_edit/<int:id>/', views.haber_edit, name='haber_edit'),
    path('haber_delete/<int:id>/', views.haber_delete, name='haber_delete'),
   # path('<int:question_id>/', views.detail, name='detail'),

]