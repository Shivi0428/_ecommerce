from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name="home"),
    #path('', include('app.urls')),
    # path('product-detail', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('plus-cart/', views.plus_cart, name='plus_cart'),
    path('minus-cart/', views.minus_cart, name='minus_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('removecart/', views.remove_cart),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name="password_reset_complete"),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('search/', views.search_results, name='search_results'),
    path('instance_comparison/', views.VirtualMachineComparisonView.as_view(), name='instance_comparison'),
    #path('instance-comparison-database/', views.instance_comparison_database_view, name='instance_comparison_database'),
# Example with app namespace
    path('instance-comparison-database/', views.instance_comparison_database_view, name='instance_comparison_database'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
