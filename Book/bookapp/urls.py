from django.urls import include, path
from django.contrib.auth.views import ( LoginView,
                                        LogoutView,
                                        PasswordResetView,
                                        PasswordResetDoneView,
                                        PasswordResetConfirmView,
                                        PasswordResetCompleteView)
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="index"),
    path('login/', LoginView.as_view(template_name='bookapp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup', views.signup , name="signup"),
    path('change_password', views.change_password,name="change_password"),
    path('reset_password', PasswordResetView.as_view(),name="reset_password"),
    path('password_reset_done',PasswordResetDoneView.as_view(),name="password_reset_done" ),
    path('password_reset_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('profile', views.profile, name="profile"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path('loggedin/', views.loggedin, name="loggedin"),
    path('buy',views.Book_to_buy.as_view(), name="buy"),
    path('details/<int:pk>', views.Book_details.as_view(), name="details"),
    path('delete/<int:pk>', views.delete, name="delete"),
    path('sell', views.Sell_book_view.as_view(), name="sell"),
    path('<int:pk>/edit', views.edit_book, name="edit"),
    path('sendmail/<int:pk>', views.sendmail, name="send_mail")
]