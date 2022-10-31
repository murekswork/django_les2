from django.urls import path, include
from .views import *
from accounts.views import DeleteProductView

urlpatterns = [
    path('', HomePageView, name='home'),
    path('shop/', ShopPageView, name='shop'),
    path('profile/cart/', CartPageView, name='cart'),
    path('profile/cart/<int:purchase_id>/delete', DeleteFromCartView, name='delete_from_cart'),
    path('product/add', AddProductView, name='product_add'),
    path('product/<int:product_id>/', ProductPageView, name='product_page'),
    path('product/<int:product_id>/delete', DeleteProductView, name='product_delete'),
    path('product/<int:product_id>/edit/', ProductEditView, name='product_edit'),
    path('profile/<int:profile_id>/visit/', ProfileVisitView, name='profile_visit'),
    path('profile/profile/purchases/<int:purchase_id>/review/', LeaveReviewView, name='review'),
]
