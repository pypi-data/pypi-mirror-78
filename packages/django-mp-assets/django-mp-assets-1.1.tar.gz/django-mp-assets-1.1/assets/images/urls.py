
from django.urls import path

from assets.images import views


app_name = 'images'


urlpatterns = [

    path('upload/<int:content_type_id>/', views.upload_image, name='upload')


]
