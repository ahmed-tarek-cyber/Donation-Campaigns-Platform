from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('home/', views.posts, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    path('add_to_cart/<int:post_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),

    path('cart/', views.cart, name='cart'),
    path('update_amount/<int:item_id>/', views.update_amount, name='update_amount'),   
    path('checkout/', views.checkout, name='checkout'),

    path('top-donors/', views.top_donors, name='top_donors'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
]
