from django.contrib import admin
from django.urls import path
from unichat import views


urlpatterns = [
    path('', views.home, name='home'),
    path('uniler', views.uniler, name='uniler'),
    path('ballar/<int:group>/', views.show_scores, name='ballar'),
    path('ballar-5/', views.show_scores_5th_group, name='ballar-5'),
    path('ballar-kollec', views.show_scores_kollec, name='ballar-kollec'),
    path('about', views.about, name="about"),
    path('teklif', views.teklif, name="teklif"),
    path('oyun', views.game, name='game'),
    path('istifadeci_serti', views.istifadeci_serti, name='istifadeci_serti'),
    path('privacy', views.privacy, name='privacy')
]
