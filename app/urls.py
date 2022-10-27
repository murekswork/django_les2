from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePageView, name='home'),
    path('shop/', ShopPageView, name='shop'),
    path('product/add', AddProductView, name='product_add'),
    path('product/<int:product_id>/', ProductPageView, name='product_page'),
    path('product/<int:product_id>/edit/', ProductEditView, name='product_edit'),
    path('profile/<int:profile_id>/visit/', ProfileVisitView, name='profile_visit'),
    path('profile/profile/purchases/<int:purchase_id>/review/', LeaveReviewView, name='review'),
]