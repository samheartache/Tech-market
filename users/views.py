from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView
from django.template.loader import render_to_string

from users.forms import LoginForm, SignUpForm, EditProfileForm
from cart.models import Cart
from products.models import Product
from users.models import User, Review


class UserLogin(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self):
        redirected_page = self.request.POST.get('next', None)
        if redirected_page and redirected_page != reverse_lazy('user:logout'):
            return redirected_page
        return reverse_lazy('main:index')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в аккаунт'
        return context


class UserRegister(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            
            return HttpResponseRedirect(self.success_url)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в аккаунт'
        return context


class UserAccount(LoginRequiredMixin, TemplateView):
    template_name = 'account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой аккаунт'


class UserEdit(LoginRequiredMixin, UpdateView):
    template_name = 'editprofile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('user:account')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context


class SendReviewView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        print(product_id)
        reviewed_product = Product.objects.get(id=product_id)
        user = User.objects.get(id=request.user.id)
        review = request.POST.get('text')
        rating = request.POST.get('rating')
        Review.objects.create(content=review, rating=rating, user=user, product=reviewed_product)

        reviews_page = render_to_string('includes/include_reviews.html', context={'reviews': Review.objects.filter(product=reviewed_product)}, request=request)
        response = {
            'reviews_page': reviews_page,
        }

        return JsonResponse(response)



@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))