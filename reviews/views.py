from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.template.loader import render_to_string


from products.models import Product
from users.models import User
from reviews.models import Review

class SendReviewView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        reviewed_product = Product.objects.get(id=product_id)
        user = User.objects.get(id=request.user.id)
        review = request.POST.get('text')
        rating = request.POST.get('rating')
        Review.objects.create(content=review, rating=rating, user=user, product=reviewed_product)

        reviews_page = render_to_string('includes/include_reviews.html', context={'reviews': Review.objects.filter(product=reviewed_product), 'user_has_review': True}, request=request)
        response = {
            'reviews_page': reviews_page,
        }

        return JsonResponse(response)


class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        review_id = request.POST.get('review_id')
        is_users_reviews_page = int(request.POST.get('flag'))

        review = Review.objects.get(id=review_id)
        product = review.product
        review.delete()

        reviews_page = render_to_string('includes/include_reviews.html', context={'reviews': Review.objects.filter(product=product), 'user_has_review': False}, request=request)
        user_reviews_page = render_to_string('includes/include_user_reviews.html', context={'reviews': Review.objects.filter(user=request.user)}, request=request) if is_users_reviews_page else 0

        response = {
            'reviews_page': reviews_page,
            'user_reviews_page': user_reviews_page,
        }

        return JsonResponse(response)


class UserReviewsView(LoginRequiredMixin, TemplateView):
    template_name = 'user_reviews.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваши отзывы'
        context['reviews'] = Review.objects.filter(user=self.request.user)
        return context