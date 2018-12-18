from django.urls import reverse
from django.core.mail import send_mail
from .spyder import OlxSpyder

from olxstat.celery import app


@app.task(bind=True, max_retries=3)
def olx_stat_task(pk, url):
    bot = OlxSpyder(thread_number=2)
    bot.add_submarketpk(pk)
    bot.add_url(url)
    bot.run()
