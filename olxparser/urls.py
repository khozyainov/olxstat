from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('submarket/<int:pk>', views.SubmarketView.as_view(), name='submarket'),

]
