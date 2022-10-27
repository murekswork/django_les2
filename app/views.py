from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm, PurchaseForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Product, Purchase, PurchaseReview
from django.db.models import Avg
from django.db import transaction
from accounts.models import Profile



def HomePageView(request):
    return render(request, template_name='home.html')


def ProductPageView(request, product_id):
    product = Product.objects.get(id=product_id)
    form = PurchaseForm()
    context = {'product': product,
               'form': form,
               'sales': len(Purchase.objects.filter(product=product))}

    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            if product.value < int(form.cleaned_data['value']):
                return redirect('shop')
            with transaction.atomic():
                purchase_filled = form.save(commit=False)
                # purchase_filled.review_id = Review(purchase_id=purchase_filled.id)
                # purchase_filled = purchase(buyer=request.user.profile,
                #                            saler=product.profile,
                #                            product=product)

                purchase_filled.buyer = request.user.profile
                purchase_filled.saler = product.profile
                purchase_filled.product = product

                purchase_price = purchase_filled.get_total_price()
                if purchase_price > purchase_filled.buyer.balance:
                    return redirect('profile')

                product.value -= purchase_filled.value
                product.save()

                buyer = purchase_filled.buyer
                buyer.balance -= purchase_price
                buyer.save()

                saler = purchase_filled.saler
                saler.balance += purchase_price
                saler.save()

                purchase_filled.save()

    return render(request, template_name='products/product.html', context=context)


def ShopPageView(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name='products/shop.html', context=context)


def ProfileVisitView(request, profile_id):
    profile = Profile.objects.get(user_id=profile_id)
    profile_products = profile.product_set.select_related()
    context = {'profile': profile,
               'products': profile_products,
               'rating': profile_products.aggregate(Avg('rating')),
               'sales': len(Purchase.objects.filter(saler=profile)),
               'products_len': len(profile_products)}

    return render(request, template_name='profile_visit.html', context=context)


def ProductEditView(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm()
    if request.method == 'POST' and product.profile == request.user.profile:
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
            return redirect('profile')
    form = ProductForm()
    return render(request, template_name='products/product_add.html', context={'form': form})


@login_required
def LeaveReviewView(request, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
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

# Create your views here.
