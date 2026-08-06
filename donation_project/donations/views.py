from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from .models import UserProfile   
from .forms import SimpleSignupForm, PostForm
from .models import Post, Cart, CartItem, Donation
from django.utils import timezone


 
def get_cart_count(user):
    if user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
        return CartItem.objects.filter(cart=cart).count()
    return 0

def signup(request):
    success_message = None
    if request.method == 'POST':
        form = SimpleSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data.get('email', '')
            mobile_phone = form.cleaned_data.get('mobile_phone', '')
            password = form.cleaned_data['password1']
            
             
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
             
            UserProfile.objects.create(user=user, mobile_phone=mobile_phone)
            
            form = SimpleSignupForm()
            success_message = "Account created successfully"
            return render(request, 'signup.html', {'form': form, 'success': success_message})
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SimpleSignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')   
        else:
            message = "Invalid username or password"
    return render(request, 'login.html', {'error': message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def posts(request):
     
    posts_qs = Post.objects.all().order_by('-id')
    cart_count = get_cart_count(request.user)
    return render(request, 'posts.html', {'posts': posts_qs, 'cart_count': cart_count})

@login_required
def search(request):
    q = request.GET.get('q', '').strip()
    date_str = request.GET.get('date', '').strip()

    posts_qs = Post.objects.all().order_by('-id')

    if q:
        posts_qs = posts_qs.filter(title__icontains=q)

    if date_str:
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            posts_qs = posts_qs.filter(created_at__date=date_obj)
        except ValueError:
            pass

    cart_count = get_cart_count(request.user)
    return render(request, 'posts.html', {'posts': posts_qs, 'cart_count': cart_count})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    cart_count = get_cart_count(request.user)
    return render(request, 'post_detail.html', {'post': post, 'cart_count': cart_count})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            return redirect('home')
    else:
        form = PostForm()
    cart_count = get_cart_count(request.user)
    return render(request, 'create_post.html', {'form': form, 'cart_count': cart_count})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    cart_count = get_cart_count(request.user)
    return render(request, 'edit_post.html', {'form': form, 'cart_count': cart_count})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('home')

@login_required
def add_to_cart(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    now = timezone.now()

    referer = request.META.get('HTTP_REFERER', '/home/')

    if post.start_time and now < post.start_time:
        return redirect(referer)

    if post.end_time and now > post.end_time:
        return redirect(referer)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    CartItem.objects.get_or_create(cart=cart, post=post, defaults={'amount': 0})

    return redirect(referer)



@login_required
def cart(request):
     
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    cart_count = get_cart_count(request.user)
    total = sum(item.amount or 0 for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total, 'cart_count': cart_count})

@login_required
def update_amount(request, item_id):
     
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except:
            data = {}
        amount = data.get('amount', '')
        try:
            amount_val = float(amount) if amount not in (None, '') else 0.0
        except:
            amount_val = 0.0
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.amount = amount_val
        item.save()
        return JsonResponse({'status': 'ok', 'amount': item.amount})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        CartItem.objects.filter(cart=cart).delete()
    return redirect('cart')

@login_required
def checkout(request):
     
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.amount or 0 for item in items)

    if request.method == 'POST' and request.POST.get('confirm_checkout'):
        for item in items:
            if item.amount and item.amount > 0:
                 
                Donation.objects.create(donor=request.user, post=item.post, amount=item.amount)
                 
                try:
                    item.post.current_amount += item.amount
                    item.post.save()
                except:
                    pass
         
        CartItem.objects.filter(cart=cart).delete()
        return redirect('home')

    cart_count = get_cart_count(request.user)
    return render(request, 'checkout.html', {'total': total, 'cart_count': cart_count})

@login_required
def top_donors(request):
    users = User.objects.all()
    donor_list = []
    for u in users:
        total = 0
        ds = Donation.objects.filter(donor=u)
        for d in ds:
            total += d.amount
        if total > 0:
             
            display_name = f"{u.first_name} {u.last_name}".strip()
            if not display_name:   
                display_name = u.username
            donor_list.append({'name': display_name, 'total': total})
    donor_list.sort(key=lambda x: x['total'], reverse=True)
    cart_count = get_cart_count(request.user)
    return render(request, 'top_donors.html', {'donors': donor_list, 'cart_count': cart_count})

def about(request):
    return render(request, 'about.html')
