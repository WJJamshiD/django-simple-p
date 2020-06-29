from django.urls import path
from . import views


urlpatterns = [
    path('<int:id>/',views.comment_thread, name='comment_thread'),
    path('<int:id>/delete',views.comment_delete, name='comment_delete'),
]
