from django.urls import path
from authentication.views import (SignUpView, login_view, refresh_token_view, LogoutAPIView,
                                UserProfileAPIView, UserListAPIView,
                                )


urlpatterns = [
    # Authentication URLs
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('refresh-token/', refresh_token_view, name='refresh_token'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    # User List URLs For Admin
    path('user-list/', UserListAPIView.as_view(), name='user_list'),

    # User Profile URLs
    path('user-profile/', UserProfileAPIView.as_view(), name='user_profile'),
]