from django.urls import path
from django.conf.urls import url
from myapp import views
from django.contrib.auth import views as auth_views


app_name = 'myapp'

urlpatterns = [
    # path(r'', views.index, name='index'),
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'about', views.about, name='about'),
    # path(r'<int:book_id>', views.detail, name='detail'),
    path(r'<int:book_id>/', views.DetailView.as_view(), name='detail'),
    path(r'findbooks', views.findbooks, name='findbooks'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'review', views.review, name='review'),
    path(r'register', views.register, name='register'),
    path(r'login',views.user_login,name='user_login'),
    path(r'logout',views.user_logout,name='user_logout'),
    path(r'password_reset/',auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html'),name='password_reset'),
    path(r'password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'),name='password_reset_done'),
    #path(r'password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView,name='password_reset_confirm'),
    path(r'chk_reviews/<int:book_id>', views.chk_reviews, name='chk_reviews'),
    path(r'check_list', views.check_list, name='check_list'),
    path(r'myorders', views.myorders, name='myorders')
    ]
