from django.urls import path
from .views import estimate_pdf, estimate_list, estimate_create, estimate_update, estimate_change_status

urlpatterns = [
    path('', estimate_list),
    path('create/', estimate_create),
    path('update/<int:pk>/', estimate_update),
    path('change-status/<int:pk>/<str:status>/', estimate_change_status),
    path('estimate/<int:pk>/pdf/', estimate_pdf),
]