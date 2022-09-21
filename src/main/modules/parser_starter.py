import json

import requests
from bs4 import BeautifulSoup

from main.models import MetricsModel, Task, CommentsModel, TaskResult
from main.models.states import MetricsNameModel


def record_rating(task, rating_before, content, rating_id):
    split_string = rating_before.split('/')
    item = split_string[0].strip()
    print(item)

    metrics = MetricsModel(task=task, link=content, metrics_name=rating_id, value=item)
    metrics.save()


def record_movie_comments(task, page_numbers, forum_page, content):
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

                comments = CommentsModel(task=task, link=content, comment=text, author=author, published_date=date)
                comments.save()

        except Exception:
            pass


def record_post_comments(task, comment_user_list, comment_text_list, content):
    for user, text in zip(comment_user_list, comment_text_list):
        try:
            author = user.find('strong').text
            date = user.find('span', class_='comment_datetime').text
            comment_text = text.text
            print('comment added')

        except Exception:
            pass

        comments = CommentsModel(task=task, link=content, comment=comment_text, author=author, published_date=date)
        comments.save()


def parser_starter(task_id, lk_id, items):
    print('start')
    task = Task.objects.get(id=task_id)
    task.status_id = 2
    task.lk_id = lk_id
    task.save()

    print(f"Send data to LK")
    try:
        LK_URL = f'https://test.core.uzavr.ru/api/v1/task/{lk_id}'
        status_dic = {"status": "queue"}
        requests.patch(url=LK_URL, json=status_dic)
    except Exception as e:
        print(f"Exception in PATCH requst {e}")


    rating_id = MetricsNameModel.objects.get(id=1)

    try:
        LK_URL = f'https://test.core.uzavr.ru/api/v1/task/{lk_id}'
        status_dic = {"status": "performing"}
        requests.patch(url=LK_URL, json=status_dic)
    except Exception as e:
        print(f"Exception in PATCH requst {e}")

    for content in items:
        try:
            if '/news/' in content:
                try:
                    link = content + 'forum/'
                    response = requests.get(link).text
                    soup = BeautifulSoup(response, 'lxml')

                    comment_user_list = soup.find_all('div', class_='comment_user')
                    comment_text_list = soup.find_all('div', class_='comment_text_full')

                except Exception:
                    comment_user_list = None
                    comment_text_list = None
                    print('no comments')

                if comment_user_list is not None and comment_text_list is not None:
                    record_post_comments(task, comment_user_list, comment_text_list, content)

            elif '/movie/' in content:

                try:
                    response = requests.get(content).text
                    soup = BeautifulSoup(response, 'lxml')
                    rating = soup.find(class_='rating_block').find('span').text
                    record_rating(task, rating, content, rating_id)

                except Exception:
                    print('no reactions')

                try:
                    link = content[:-6] + 'forum/'
                    forum_page = requests.get(link).text
                    soup = BeautifulSoup(forum_page, 'lxml')
                    page_numbers = int(soup.find(class_='page_numbers').find_all('a')[-2].text)

                except Exception:
                    page_numbers = 1

                try:
                    record_movie_comments(task, page_numbers, link, content)

                except Exception:
                    pass

            else:
                print('continue')

        except Exception:
            print('wrong link')

            try:
                task.status_id = 4
                task.save()
                LK_URL = f'https://test.core.uzavr.ru/api/v1/task/{lk_id}'
                status_dic = {"statusCode": 400, "message": ["This login(link) cannot be parsed"],
                              "error": "Wrong login", "status": "error"}
                status_dic = {"status": "error"}
                requests.patch(url=LK_URL, json=status_dic)
            except Exception as e:
                print(f"Exception in PATCH requst {e}")

    metrics_result = MetricsModel.objects.filter(task_id=task_id)
    comments_result = CommentsModel.objects.filter(task_id=task_id)
    print(metrics_result)
    print(comments_result)
    result_for_lk = {"pattern": "", "data": ""}
    if metrics_result.exists() or comments_result.exists():
        result_list = []

        d = {'taskId': lk_id, 'type': '', 'login': '', 'data': ''}

        if metrics_result.exists():
            for res in metrics_result:
                d['link'] = res.link
                d['metrics_id'] = res.metrics_name.pk
                d['value'] = res.value

        if comments_result.exists():
            comments = []
            d['type'] = "16"
            d['login'] = comments_result[0].link
            for res in comments_result:
                comments_dic = {}
                comments_dic['author'] = res.author
                comments_dic['text'] = res.comment
                comments_dic['published_date'] = res.published_date

                comments.append(comments_dic)

            d['data'] = comments
            result_for_lk['pattern'] = "new_response"
            result_for_lk['data'] = d

            try:
                connection = pika.BlockingConnection(pika.URLParameters('amqp://rmq:t87VxFvCSYLK@130.193.43.169:45672'))
                channel = connection.channel()
                channel.queue_declare(queue='results', durable=True)
                channel.basic_publish(exchange='results', routing_key='result', body=json.dumps(result_for_lk))
                channel.start_consuming()
                task.status_id = 3
                task.save()

            except Exception:
                print("RabitMq error")

        print(d)
        result_list.append(d)

        with open(f"files/task__{task_id}.json", "w", encoding='utf-8') as write_file:
            json.dump(result_for_lk, write_file, ensure_ascii=False)

        TaskResult.objects.create(task_id=task_id, link=f"task__{task_id}.json", comment=None)

    else:
        TaskResult.objects.create(task_id=task_id, link=None, comment='Failed to receive metrics and comments')

    task.status_id = 3
    task.save()

    if task.status_id == 3:
        try:
            LK_URL = f'https://test.core.uzavr.ru/api/v1/task/{lk_id}'
            status_dic = {"status": "completed"}
            requests.patch(url=LK_URL, json=status_dic)
        except Exception as e:
            print(f"Exception in POST requst {e}")

    print('end')
