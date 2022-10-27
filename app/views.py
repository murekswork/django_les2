from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Product
from accounts.models import Profile


def HomePageView(request):
    return render(request, template_name='home.html')


def ProductPageView(request, product_id):

    return render(request, template_name='products/product.html', context={'product':Product.objects.get(id=product_id)})


def ShopPageView(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, template_name='products/shop.html', context=context)


def ProfileVisitView(request, profile_id):
    profile = Profile.objects.get(user_id=profile_id)
    profile_products = profile.product_set.select_related()
    context = {'profile': profile,
               'products': profile_products}

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
# Create your views here.
