from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Product, UserProfile
from .forms import ProductForm, RegisterForm, ProfileForm


def home(request):

    products = Product.objects.all().order_by('-id')

    return render(request, 'home.html', {
        'products': products
    })


def custom_login(request):

    if request.method == 'POST':

        login_type = request.POST.get('login_type')
        password = request.POST.get('password')

        username = None

        # LOGIN WITH EMAIL
        if login_type == 'email':

            email = request.POST.get('email')

            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username

            except User.DoesNotExist:

                messages.error(request, 'Email Not Found')

                return redirect('login')

        # LOGIN WITH USERNAME
        else:

            username = request.POST.get('username')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request, 'Login Successful')

            return redirect('/')

        else:

            messages.error(request, 'Invalid Credentials')

            return redirect('login')

    return render(request, 'login.html')


@login_required
def create_product(request):

    if request.method == 'POST':

        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)

            product.user = request.user

            product.save()

            messages.success(request, 'Product Added Successfully')

            return redirect('/')

    else:

        form = ProductForm()

    return render(request, 'product_form.html', {
        'form': form
    })


@login_required
def edit_product(request, id):

    product = get_object_or_404(Product, id=id)

    if product.user != request.user:

        messages.error(request, 'Unauthorized Access')

        return redirect('/')

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product
    )

    if form.is_valid():

        form.save()

        messages.success(request, 'Product Updated Successfully')

        return redirect('/')

    return render(request, 'product_form.html', {
        'form': form
    })


@login_required
def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    if product.user != request.user:

        messages.error(request, 'Unauthorized Access')

        return redirect('/')

    if request.method == 'POST':

        product.delete()

        messages.success(request, 'Product Deleted Successfully')

        return redirect('/')

    return render(request, 'product_delete.html', {
        'product': product
    })


def register_user(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            # CHECK EMAIL ALREADY EXISTS
            if User.objects.filter(
                email=form.cleaned_data['email']
            ).exists():

                messages.error(
                    request,
                    'Email Already Exists'
                )

                return redirect('register')

            # SAVE USER
            user = form.save()

            # LOGIN USER
            login(request, user)

            # SEND WELCOME EMAIL
            html_message = render_to_string(
                'emails/welcome_email.html',
                {
                    'user': user,
                    'site_url': request.build_absolute_uri('/'),
                }
            )

            email = EmailMultiAlternatives(
                'Welcome to Inventory Project',
                strip_tags(html_message),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.attach_alternative(html_message, 'text/html')
            email.send(fail_silently=False)

            messages.success(
                request,
                'Registration Successful'
            )

            return redirect('/')

    else:

        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })


@login_required
def profile_view(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, 'profile.html', {
        'profile': profile
    })


@login_required
def edit_profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Profile Updated Successfully'
        )

        return redirect('profile')

    return render(request, 'edit_profile.html', {
        'form': form
    })


@login_required
def request_delete_account(request):

    user = request.user

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = default_token_generator.make_token(user)

    delete_link = request.build_absolute_uri(
        f'/delete-account-confirm/{uid}/{token}/'
    )

    send_mail(
        'Delete Account Confirmation',
        f'Hello {user.username},\n\n'
        f'Click this link to delete your account:\n\n'
        f'{delete_link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    messages.success(
        request,
        'Confirmation email sent to your email.'
    )

    return redirect('profile')


def confirm_delete_account(request, uidb64, token):

    UserModel = get_user_model()

    try:

        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = UserModel.objects.get(pk=uid)

    except (
        TypeError,
        ValueError,
        OverflowError,
        UserModel.DoesNotExist
    ):

        user = None

    if user is not None and default_token_generator.check_token(user, token):

        if request.method == 'POST':

            user.delete()

            messages.success(
                request,
                'Account Deleted Successfully'
            )

            return redirect('/')

        return render(request, 'confirm_delete_account.html', {
            'user_obj': user
        })

    else:

        messages.error(
            request,
            'Invalid Delete Link'
        )

        return redirect('/')
