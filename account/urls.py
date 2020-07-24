from django.urls import path

from .views import LoginView, RegisterView, ConfirmRegistrationView, Logout

app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ConfirmRegistrationView.as_view(), name='activate'),
    path('logout/', Logout.as_view(), name="logout")

]