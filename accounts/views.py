import operator

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import SignUpForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg
from .models import Profile
from app.models import Product, Purchase
from django.contrib import messages


def AccountOverviewView(request):
    if not request.user.is_authenticated:
        return redirect('home')
    profile = request.user.profile
    products = request.user.profile.product_set.select_related()
    rating = products.aggregate(Avg('rating'))
    context = {'profile': profile,
               'products': products,
               'purchases': Purchase.objects.order_by('-date').filter(buyer=profile),
               'products_len': len(products),
               'rating': rating['rating__avg']}
    return render(request, template_name='account_overview.html', context=context)


def DeleteProductView(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect('profile')



@login_required
def UpdateProfileView(request):
    profile_id = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = profile_id.user
            profile.balance = Profile.objects.get(user=profile_id).balance
            profile.save()
            messages.success(request, f'Profile info successfully saved!')
            return redirect('profile')
        messages.error(request, f'Error! Invalid account info, try again.')
    form = ProfileForm()
    return render(request, template_name='profile_update.html', context={'form': form})

def SignUpView(request):
    if request.user.is_authenticated:
        messages.error(request, f'You already logged in!')
        return redirect('profile')
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                new_profile = Profile(user_id=user.id)
                new_profile.save()
                print(user.username, form.cleaned_data['password'])
                authentication = authenticate(username=user.username, password=form.cleaned_data['password'])
                login(request, authentication)
                messages.success(request, f'You signed up as {request.user.username}, now you can setup account info!')
            return redirect('profile')
        messages.error(request, 'Invalid username or password, try again!')
        form = SignUpForm()
    return render(request, template_name='registration/signup.html', context={'form': form})
# Create your views here.
