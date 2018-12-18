from django.urls import reverse
from django.core.mail import send_mail
from .spyder import OlxSpyder
from .models import Submarket

from olxstat.celery import app
from celery import chain

@app.task
def run_stat_task(pk, url):
    chain(olx_stat_task.s(pk, url), send_email_task.s()).apply_async()


@app.task
def olx_stat_task(pk, url):
    bot = OlxSpyder(thread_number=2)
    bot.add_submarketpk(pk)
    bot.add_url(url)
    bot.run()
    return pk

@app.task
def send_email_task(pk):
    submarket = Submarket.objects.get(pk=pk)
    email = submarket.email
    link = '127.0.0.1:8000'+submarket.get_absolute_url()
    send_mail(
        'Olx statistics',
        f'Hello, you got statistics {link}',
        'olxstat@no-reply.org',
        [email],
        fail_silently=False,
    )
