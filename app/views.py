from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm, PurchaseForm, ReviewForm, FilterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Purchase, PurchaseReview, Cart
from django.db.models import Avg
from django.db import transaction
from accounts.models import Profile
from django.views.generic import TemplateView, ListView, View
from django.contrib import messages

import operator



def HomePageView(request):

    products = Product.objects.order_by('-purchase_len')[:5]
    products = sorted(products, key=operator.attrgetter('rating'), reverse=True)[:5]
    context = {'top': products}
    return render(request, template_name='home.html', context=context)


def ProductPageView(request, product_id):
    """
    Tries to get product object from database and sets it in context.
    Calls PurchaseForm from forms module.
    """
    product = get_object_or_404(Product, id=product_id)
    form = PurchaseForm()
    context = {'product': product,
               'form': form,
               'purchases': product.purchase_set.select_related()}

    # if request.method == 'GET':
    if request.method == 'POST':
        """
        Checks for (buy) or (add to cart) response in request.
        """
        if not request.user.profile == product.profile:
            form = PurchaseForm(request.POST)
            if 'buy' in request.POST:
                if form.is_valid():
                    if not product.value < int(form.cleaned_data['value']):
                        with transaction.atomic():
                            purchase_filled = form.save(commit=False)
                            # purchase_filled.review_id = Review(purchase_id=purchase_filled.id)
                            # purchase_filled = purchase(buyer=request.user.profile,
                            #                            saler=product.profile,
                            #                            product=product)

                            purchase_filled.buyer = request.user.profile
                            purchase_filled.saler = product.profile
                            purchase_filled.product = product
                            """
                            Checks if profile has enough money for this purchase
                            """
                            purchase_filled.get_total_price()
                            if purchase_filled.total_price <= request.user.profile.balance:
                                purchase_filled.save()
                                purchase_filled.make_payment()
                                purchase_filled.save()
                                messages.success(request, f'Successfully bought {purchase_filled.product.name}')
                                return redirect('profile')
                            else:
                                messages.error(request, 'Not enough money!')
                    else:
                        messages.error(request, 'Not enough products!')
            elif 'cart' in request.POST:

                if form.is_valid():

                    """
                    Checks if user has created cart and create it if not
                    """
                    if Cart.objects.filter(profile=request.user.profile).exists():
                        cart = Cart.objects.get(profile=request.user.profile)
                    else:
                        cart = Cart(profile=request.user.profile)
                        cart.save()

                    """
                    Checks if product already in cart
                    """
                    if request.user.profile.cart.purchase_set:
                        if request.user.profile.cart.purchase_set.filter(product=product).exists():
                            messages.error(request, 'This product already in cart!')
                            return redirect('cart')

                    """
                    Checks if product available value more than purchase value
                    """
                    if not form.cleaned_data['value'] > product.value:
                        with transaction.atomic():
                            add_purchase_to_cart = form.save(commit=False)

                            add_purchase_to_cart.buyer = request.user.profile
                            add_purchase_to_cart.saler = product.profile
                            add_purchase_to_cart.product = product
                            add_purchase_to_cart.get_total_price()

                            if Cart.objects.get(profile=request.user.profile):
                                cart = Cart.objects.get(profile=request.user.profile)
                            else:
                                cart = Cart(profile=request.user.profile)
                                cart.save()

                            add_purchase_to_cart.cart = cart
                            add_purchase_to_cart.save()
                        messages.success(request, f'Product {add_purchase_to_cart.product.name} '
                                                  f'X{add_purchase_to_cart.value} added to cart')
                        return redirect('cart')
                    else:
                        messages.error(request, 'Not enough value!')
                    # purchase_price = purchase_filled.get_total_price()
                    # if purchase_price > purchase_filled.buyer.balance:
                    #     return redirect('profile')
                    #
                    # product.buy(value=purchase_filled.value)
                    # product.save()
                    #
                    # buyer = purchase_filled.buyer
                    # buyer.balance -= purchase_price
                    # buyer.save()
                    #
                    # saler = purchase_filled.saler
                    # saler.balance += purchase_price
                    # saler.save()
                    #
                    # purchase_filled.save()
        else:
            messages.error(request, 'You cant buy your own product!')
            # messages.add_message(request, messages.ERROR, 'You cant buy your own product')

    return render(request, template_name='products/product.html', context=context)


# class ShopPageView(View):
#     model = Product
#     template_name = 'products/shop.html'
#     context = {'products': model.objects.all()}
#
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context[]
#     def get(self, request):
#         filter = request.GET.get('filter')
#         if filter:
#             self.context['products'] = sorted()

def ShopPageView(request):
    products = Product.objects.all()
    form = FilterForm()
    context = {'products': sorted(products, key=operator.attrgetter('id'), reverse=True),
               'form': form}
    if request.method == 'GET':
        filter = request.GET.get('filter')
        if filter:
            context['products'] = sorted(products, key=operator.attrgetter(filter), reverse=True)
        # print(filter_value)
        # if filter_value == 'PRICE':
        #     return render(request, template_name='products/shop.html', context={'products:' : sorted(products, key=operator.attrgetter('price'))})


    return render(request, template_name='products/shop.html', context=context)


def ProfileVisitView(request, profile_id):
    # profile = Profile.objects.get(user_id=profile_id)
    profile = get_object_or_404(Profile, user_id=profile_id)
    profile_products = profile.product_set.select_related()
    context = {'profile': profile,
               'products': profile_products,
               'rating': round((profile_products.aggregate(Avg('rating'))['rating__avg']), 2),
               'sales': len(Purchase.objects.filter(saler=profile)),
               'products_len': len(profile_products)}

    return render(request, template_name='profile_visit.html', context=context)


def ProductEditView(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # product = Product.objects.get(id=product_id)
    if product.profile != request.user.profile:
        messages.info(request, 'It is not your product!')
        return redirect('profile')
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            edit_product = form.save(commit=False)
            edit_product.rating = product.rating
            edit_product.id = product.id
            edit_product.profile = product.profile
            edit_product.save()
        return redirect('product_page', product_id=product_id)
    form = ProductForm()
    context = {'form': form}
    return render(request, template_name='products/product_edit.html', context=context)


@login_required
def AddProductView(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.profile = request.user.profile
            product.save()
            messages.success(request, f'{product} successfully uploaded to marketplace')
            return redirect('product_page', product_id=product.id)
        messages.error(request, 'Something went wrong!')
    form = ProductForm()
    return render(request, template_name='products/product_add.html', context={'form': form})


@login_required
def LeaveReviewView(request, purchase_id):
    # purchase = Purchase.objects.get(id=purchase_id)
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if purchase.buyer != request.user.profile:
        return redirect('profile')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                review = form.save(commit=False)
                review.product = purchase.product
                review.save()

                purchase.review = review
                purchase.save()

                product = Product.objects.get(id=purchase.product.id)
                product.rating = purchase.product.purchasereview_set.select_related().aggregate(Avg('rating'))['rating__avg']
                product.save()
                return redirect('profile')

    form = ReviewForm()
    return render(request, template_name='products/review.html', context={'form': form})


def CartPageView(request):
    if Cart.objects.filter(profile=request.user.profile).exists():
        cart = Cart.objects.get(profile=request.user.profile)
    else:
        cart = Cart(profile=request.user.profile)
        cart.save()

    cart.get_cart_total_price()
    cart.save()
    context = {'cart': cart}

    if 'checkout' in request.POST:
        with transaction.atomic():
            cart_transaction = cart.proc_checkout()
            if cart_transaction['success']:
                messages.success(request, 'Proceed checkout!')
                return redirect('profile')
            else:
                messages.error(request, f'{cart_transaction["error"]}')

    return render(request, template_name='cart.html', context=context)


def DeleteFromCartView(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    purchase.delete()
    messages.error(request, f'Product {purchase.product} removed from cart!')
    return redirect('cart')

    # cart = request.user.cart
    # return render(request, template_name='products/cart.html', context={'cart': cart})

# Create your views here.
