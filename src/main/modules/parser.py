from datetime import datetime

import requests
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup
from peewee import MySQLDatabase, Model, IntegerField, CharField, TextField, PrimaryKeyField

pg_db = MySQLDatabase(database="apiparser", user='iriparser', password='asdflk#$KGf8FD&fasdjkksdf', host='89.223.67.114',
                      port=3306, charset='utf8mb4')

class BaseModel(Model):
    class Meta:
        database = pg_db


class Comments(BaseModel):
    id = IntegerField(primary_key=True)
    comment_id = CharField(max_length=200)
    user_id = CharField(max_length=200)
    name = CharField(max_length=200)
    comment = TextField()
    comment_original = TextField()
    like_count = IntegerField()
    published = CharField(max_length=200)
    video_id_id = IntegerField()


class Metrics(BaseModel):
    id = PrimaryKeyField(null=False)
    material_id = IntegerField()
    id_metrics_name = IntegerField()
    value = CharField(max_length=255)
    time = IntegerField(default=0)


class Content(BaseModel):
    id_content = PrimaryKeyField(null=False)
    resource = CharField(max_length=255)
    created_at = IntegerField()
    project_name = CharField(max_length=255)
    id_format_content = IntegerField()
    name_content = CharField(max_length=255)
    url = CharField(max_length=255, unique=True)
    success = IntegerField(default=0)
    success_date_update = IntegerField()
    acc_type = IntegerField()


def record_rating(rating, content_id):
    split_string = rating.split('/')
    item = split_string[0].strip()
    print(item)

    Metrics.create(material_id=content_id, id_metric_name=36, value=item)


def record_movie_comments(page_numbers, forum_page, content_id):
    for page in range(1, page_numbers + 1):
        try:
            forum_page = forum_page + f'f{page}/'
            print(forum_page)
            response = requests.get(forum_page).text
            soup = BeautifulSoup(response, 'lxml')
            comments = soup.find('div', class_='comments_block').find_all('div', itemprop='review')

            if page - 10 >= 0:
                forum_page = forum_page[:-4]
            else:
                forum_page = forum_page[:-3]

            for comment in comments:
                try:

                    author = comment.find('strong', itemprop='author').text
                    date = comment.find('span', class_='comment_datetime').text
                    text = comment.find('div', class_='comment_text_full').text

                    print('comment added')

                except Exception:
                    pass

                Comments.get_or_create(comment=text, comment_original=text, video_id_id=content_id,
                                       name=author, published=date)

        except Exception:
            pass


def record_post_comments(comment_user_list, comment_text_list, content_id):
    for user, text in zip(comment_user_list, comment_text_list):
        try:
            author = user.find('strong').text
            date = user.find('span', class_='comment_datetime').text
            comment_text = text.text
            print('comment added')

        except Exception:
            pass

        Comments.get_or_create(comment=comment_text, comment_original=text, video_id_id=content_id,
                               name=author, published=date)



def parser():
    print('start')
    cur = pg_db.cursor()
    cur.execute('SELECT * from content where resource = "KINOTEATR"')
    rows = cur.fetchall()
    cur.close()

    for row in rows:
        link = row[6]

        try:
            if '/news/' in link:
                try:
                    link = link + 'forum/'
                    response = requests.get(link).text
                    soup = BeautifulSoup(response, 'lxml')

                    comment_user_list = soup.find_all('div', class_='comment_user')
                    comment_text_list = soup.find_all('div', class_='comment_text_full')

                except Exception:
                    comment_user_list = None
                    comment_text_list = None
                    print('no comments')

                if comment_user_list is not None and comment_text_list is not None:
                    record_post_comments(comment_user_list, comment_text_list, row[0])

            elif '/movie/' in link:

                try:
                    response = requests.get(link).text
                    soup = BeautifulSoup(response, 'lxml')
                    rating = soup.find(class_='rating_block').find('span').text
                    record_rating(rating, row[0])

                except Exception:
                    print('no reactions')

                try:
                    link = link[:-6] + 'forum/'
                    forum_page = requests.get(link).text
                    soup = BeautifulSoup(forum_page, 'lxml')
                    page_numbers = int(soup.find(class_='page_numbers').find_all('a')[-2].text)

                except Exception:
                    page_numbers = 1

                try:
                    record_movie_comments(page_numbers, link, row[0])

                except Exception:
                    pass

            else:
                print('continue')

        except Exception:
            print('wrong link')

    print('end')


# def parse_csv():
#     data = pd.read_csv(r'C:\Users\1\PycharmProjects\KinoTeatr\more.tv_kino.teatr.tv_fonar.tv_rutube.ru-_2_.csv', delimiter=',')
#     print(data.info())
#     for index, item in data.iterrows():
#         Content.create(resource="KINOTEATR", project_name=item['РќР°Р·РІР°РЅРёРµ РїСЂРѕРµРєС‚Р°'], id_format_content=2,
#                        name_content=item['РќР°Р·РІР°РЅРёРµ РµРґРёРЅРёС†С‹ РєРѕРЅС‚РµРЅС‚Р°'],
#                        url=item['РЎСЃС‹Р»РєР° РЅР° РєРѕРЅС‚РµРЅС‚, СЂР°Р·РјРµС‰РµРЅРЅС‹Р№ РІ РёРЅС‚РµСЂРЅРµС‚'])



scheduler = BlockingScheduler(daemon=True)
date_now = datetime.now().strftime('%H:%M:%S:%f')
print(date_now)
# from now - 3
date_time_str = '16:01:00'

date_time = datetime.strptime(date_time_str, '%H:%M:%S')
print(date_time.strftime('%H:%M:%S:%f'))
scheduler.add_job(parser, trigger=CronTrigger(hour=date_time.hour, minute=date_time.minute),
replace_existing=True)

try:
    scheduler.start()
except KeyboardInterrupt as e:
    print(e)
    scheduler.shutdown()