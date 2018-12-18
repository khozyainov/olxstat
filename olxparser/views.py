from django.shortcuts import render
from .models import Submarket, Post
from .forms import IndexForm
from django.views import generic


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
    pass
