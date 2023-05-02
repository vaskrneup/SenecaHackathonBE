from knox import views as knox_views
from user import views as user_views
from django.urls import path

app_name = "user"

urlpatterns = [
    path("api/user/auth/login/", user_views.LoginView.as_view(), name='knox_login'),
    path("api/user/auth/logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("api/user/auth/logoutall/", knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    
    path("api/user/get-user-data/", user_views.GetUserDetailsView.as_view(), name='user_detail_view'),
]
