from django.urls import path

from . import views

# Define URL patterns for the app
urlpatterns = [
    path("<slug:course_id>/lessons/<slug:lesson_id>/", views.lesson_detail_view),
    path("<slug:course_id>/", views.course_detail_view),
    path("", views.course_list_view),
]