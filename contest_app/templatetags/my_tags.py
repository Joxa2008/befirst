from django import template
from django.utils.timezone import now
from datetime import timedelta

register = template.Library()


def is_expert_checked(query_set, expert):
    if not query_set:
        return False
    else:
        my_list = []
        for i in query_set:
            my_list.append(i.expert)
        if expert not in my_list:
            return False
        return True


register.filter('is_expert_checked', is_expert_checked)


def deadline_status(deadline):
    if deadline - timedelta(hours=1) < now() and (deadline > now()):
        return 'warning'
    elif deadline - timedelta(hours=1) > now():
        return 'success'
    else:
        return 'danger'


register.filter('deadline_status', deadline_status)


def contest_order_deadline(query_set):
    return query_set.order_by('publish_date')


register.filter('order_by_deadline', contest_order_deadline)


def is_contest_completed_by_expert(query_set, expert):
    my_list = []
    counter = 0

    for work in query_set.works.all():
        counter += 1
        my_list_1 = []
        for i in work.scores.all():
            my_list_1.append(i.expert)
        if expert in my_list_1:
            my_list.append(1)

    if counter == len(my_list):
        return True
    return False


register.filter('is_all_checked', is_contest_completed_by_expert)
