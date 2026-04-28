from django.urls import path
from .views import client_list, client_detail   # ⭕ 여기 views는 같은 폴더

urlpatterns = [
    path('', client_list),
    path('<int:pk>/', client_detail),
]