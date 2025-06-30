from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

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
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                    return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в аккаунт'
        return context


class UserRegister(CreateView):
    template_name = 'suignup.html'
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
    
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.instance

#             session_key = request.session.session_key

#             auth.login(request, user)

#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)

#             return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = SignUpForm()
    
#     context = {
#         'title': 'Вход в аккаунт',
#         'form': form,
#     }
#     return render(request, 'signup.html', context)


@login_required
def account(request):
    context = {
        'title': 'Аккаунт пользователя'
    }
    return render(request, 'account.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


@login_required
def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            if 'avatar' in request.FILES:
                print(request.user.avatar)
                request.user.avatar = request.FILES['avatar']
            form.save()
            return HttpResponseRedirect(reverse('user:account'))
        else:
            print(form.errors)
    else:
        form = EditProfileForm(instance=request.user)
    
    context = {
        'title': 'Редактирование профиля',
        'form': form
    }
    return render(request, 'editprofile.html', context)