from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .models import Author


@login_required
def become_author(request):
    authors_group, _ = Group.objects.get_or_create(name='authors')

    if request.user in authors_group.user_set.all():
        messages.info(request, "Вы уже являетесь автором.")
    else:
        # 1. Добавляем в группу
        authors_group.user_set.add(request.user)

        # 2. Создаём объект Author, если ещё не существует
        Author.objects.get_or_create(user=request.user)

        messages.success(request, "Теперь вы автор и можете создавать и редактировать посты!")

    return redirect('/accounts/')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

