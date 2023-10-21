from .views import GetTokenNewRoleView, EnterMyDataView
from django.urls import path

urlpatterns = [
    path("get_token_new_role/", GetTokenNewRoleView.as_view()), # post data: { "role": "cooker" }
    path("enter_my_data/", EnterMyDataView.as_view()), # Auth Bearer b14asj4r2od...
]
