from django.shortcuts import render
from django.views.generic.edit import FormView
from .models import Submarket, Post
from .forms import IndexForm

# Create your views here.
class IndexView(FormView):
    model = Submarket
    form_class = IndexForm
    fields = ['submarketurl', 'email']
    template_name = 'index.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(IndexView, self).form_valid(form)
