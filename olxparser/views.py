from .models import Submarket
from .forms import IndexForm
from django.views import generic
import calendar

# Create your views here.
class IndexView(generic.FormView):
    model = Submarket
    form_class = IndexForm
    fields = ['submarketurl', 'email']
    template_name = 'index.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(IndexView, self).form_valid(form)

class SubmarketView(generic.DetailView):
    model = Submarket
    template_name = 'submarket.html'

    def get_context_data(self, **kwargs):
        context = super(SubmarketView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        submarket = Submarket.objects.get(pk=pk)
        posts = submarket.post_set.select_related()
        weekdays_count = {}
        hours_count = {}
        for day in range(0, 7):
            weekdays_count[day] = 0
        for hour in range(0, 24):
            hours_count[hour] = 0
        for post in posts:
            creation_datetime = post.creation_date
            weekday = creation_datetime.weekday()
            hour = int(creation_datetime.strftime('%H'))
            weekdays_count[weekday] = weekdays_count[weekday] + 1
            hours_count[hour] = hours_count[hour] + 1

        context['weekdays_x'] = [calendar.day_name[day] for day in weekdays_count.keys()]
        context['weekdays_y'] = list(weekdays_count.values())
        context['hours_x'] = list(hours_count.keys())
        context['hours_y'] = list(hours_count.values())
        return context
