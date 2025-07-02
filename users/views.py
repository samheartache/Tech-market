from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView, UpdateView

from users.forms import LoginForm, SignUpForm, EditProfileForm
from cart.models import Cart


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


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))