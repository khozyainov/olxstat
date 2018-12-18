from  grab.spider import Spider,Task
import re
import datetime
from .models import Post, Submarket

DATE_MASK = r'((?:\d|[01]\d|2[0-3]):[0-5]\d)\W\s*(3[01]|[12][0-9]|0?[1-9])\s(\w*)\s((?:19|20)\d{2})\s*'
MONTH_MAP = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}


class OlxSpyder(Spider):
    def add_url(self, url):
        self.initial_urls.append(url)

    def add_submarketpk(self, pk):
        self.submarket = Submarket.objects.get(pk=pk)

    def task_initial(self, grab, task):
        print('Start parse olx')
        last_page = int(grab.xpath_text('//a[@data-cy="page-link-last"]/span'))
        base_url = self.initial_urls[0]
        if '&page=' in base_url:
            base_url = re.sub('&page=\d*$', '', base_url)
        print(last_page)
        print(base_url)
        for page in range(1, last_page+1):
            yield Task('page', url=f'{base_url}&page={page}')

    def task_page(self, grab, task):
        print('Start parse olx')
        for elem in  grab.xpath_list('//a[@class="marginright5 link linkWithHash detailsLink"]'):
            yield Task('olxpost', url=elem.get('href'))

    def task_olxpost(self, grab, task):
        print(f'olxpost: {task.url}')
        text = grab.xpath_text('//*[@class="offer-titlebox__details"]')
        creation_date = self._get_date(text)
        print(creation_date)
        Post.objects.create(submarket=self.submarket, creation_date=creation_date)


    @staticmethod
    def _strtoint_month(strmonth):
        if strmonth in MONTH_MAP:
            return MONTH_MAP[strmonth]
        return 1

    @staticmethod
    def _get_date(text):
        p = re.compile(DATE_MASK)
        m = p.search(text)
        time = m.group(1)
        day = m.group(2)
        strmonth = m.group(3)
        month = OlxSpyder._strtoint_month(strmonth)
        year = m.group(4)
        datetime_str = f'{time} {day}-{month}-{year}'
        datetime_obj = datetime.datetime.strptime(datetime_str, '%H:%M %d-%m-%Y')
        return datetime_obj


#if __name__ == '__main__':
#    bot = OlxSpyder(thread_number=2)
#    bot.add_url('https://www.olx.ua/rabota/nachalo-karery-studenty/?search%5Bfilter_enum_job_type%5D%5B0%5D=perm&search%5Boffer_seek%5D=seek&page=2')
#   bot.run()
