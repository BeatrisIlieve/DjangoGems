from django.shortcuts import redirect
from django.views.generic import ListView
from django.views import View
from django_gems.common.mixins import NavigationBarMixin
from django_gems.jewelry.models import Jewelry
from django_gems.wishlist.models import JewelryLike


class LikeJewelryView(View):
    def get(self, request, *args, **kwargs):
        jewelry_pk = kwargs.get('jewelry_pk')

        if request.user.is_authenticated:
            user_id = request.user.pk

            kwargs = {
                'jewelry_id': jewelry_pk,
                'user_id': user_id,
            }

            user_liked_jewelry = JewelryLike.objects.filter(**kwargs).first()

            if user_liked_jewelry:
                user_liked_jewelry.delete()
            else:
                JewelryLike.objects.create(**kwargs)

        else:

            liked_jewelries = request.session.get('liked_jewelries', [])

            if jewelry_pk in liked_jewelries:
                liked_jewelries.remove(jewelry_pk)
            else:
                liked_jewelries.append(jewelry_pk)

            request.session['liked_jewelries'] = liked_jewelries

        return redirect(request.META.get('HTTP_REFERER', '/'))


class DisplayedLikedJewelries(NavigationBarMixin, ListView):
    model = Jewelry
    template_name = 'wishlist/liked_jewelries.html'
    context_object_name = 'jewelries'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:

            likes_pks = JewelryLike.objects. \
                filter(user_id=self.request.user.pk). \
                values_list('jewelry_id', flat=True)

            queryset = queryset.filter(id__in=likes_pks)

            for jewelry in queryset:
                jewelry.liked_by_user = jewelry.jewelrylike_set. \
                    filter(user=self.request.user). \
                    exists()
        else:
            liked_jewelries = self.request.session.get('liked_jewelries', [])
            likes_pks = liked_jewelries

            queryset = queryset.filter(id__in=likes_pks)

            for jewelry in queryset:
                jewelry.liked_by_user = jewelry.pk in liked_jewelries

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        count_liked_jewelries = len(self.get_queryset())

        context['count_liked_jewelries'] = count_liked_jewelries

        nav_bar_context = self.get_nav_bar_context()
        context.update(nav_bar_context)

        return context
