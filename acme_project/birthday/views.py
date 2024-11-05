from django.views.generic import (
    CreateView, DeleteView,  DetailView, ListView, UpdateView)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm, CongratulationForm
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown
from .models import Birthday


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):

    model = Birthday
    # По умолчанию этот класс
    # выполняет запрос queryset = Birthday.objects.all(),
    # но мы его переопределим:
    queryset = Birthday.objects.prefetch_related(
        'tags').select_related('author')
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


# Наследуем BirthdayCreateView от CreateView и от миксина LoginRequiredMixin:
class BirthdayCreateView(LoginRequiredMixin, CreateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # Этот класс сам может создать форму на основе модели!
    # Нет необходимости отдельно создавать форму через ModelForm.
    # Указываем поля, которые должны быть в форме:
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # после удаления объекта:
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context


# def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
#    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
#        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
#    else:
        # Связывать форму с объектом не нужно, установим значение None.
#        instance = None
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
#    form = BirthdayForm(request.POST or None,
#                         Файлы, переданные в запросе, указываются отдельно.
#                        files=request.FILES or None,
#                        instance=instance)
    # Создаём словарь контекста сразу после инициализации формы.
#    context = {'form': form}
    # Если введённые данные верны...
#    if form.is_valid():
#        form.save()
        # ...вызовем функцию подсчёта дней:
#        birthday_countdown = calculate_birthday_countdown(
#             ...и передаём в неё дату из словаря cleaned_data.
#            form.cleaned_data['birthday']
#        )
    # если в POST-запросе были переданы параметры — значит, объект request.POST
    # не пуст и этот объект передаётся в форму; если же объект request пуст
    # — срабатывает условиe or и форма создаётся без параметров,
    # через BirthdayForm(None) — это идентично обычному BirthdayForm().
    # Обновляем словарь контекста: добавляем в него новый элемент.
#        context.update({'birthday_countdown': birthday_countdown})
    # Указываем нужный шаблон и передаём в него словарь контекста.
#    return render(request, 'birthday/birthday.html', context)


# def birthday_list(request):
    # Получаем все объекты модели Birthday из БД с сортировкой по id.
#   birthdays = Birthday.objects.order_by('id')
    # Создаём объект пагинатора с количеством 10 записей на страницу.
#   paginator = Paginator(birthdays, 10)
    # Получаем из запроса значение параметра page.
#   page_number = request.GET.get('page')
    # Получаем запрошенную страницу пагинатора.
    # Если параметра page нет в запросе или его значение не приводится к числу,
    # вернётся первая страница.
#   page_obj = paginator.get_page(page_number)
    # Вместо полного списка объектов передаём в контекст шаблона
    # объект страницы пагинатора.
#   context = {'page_obj': page_obj}
#   return render(request, 'birthday/birthday_list.html', context)


# def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
#    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
#    form = BirthdayForm(instance=instance)
#    context = {'form': form}
    # Если был получен POST-запрос...
#    if request.method == 'POST':
        # ...удаляем объект:
#        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
#        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
#    return render(request, 'birthday/birthday.html', context)


# Будут обработаны POST-запросы только от залогиненных пользователей.
@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)
