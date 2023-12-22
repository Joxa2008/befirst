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
    print(deadline)
    print(deadline - timedelta(hours=1))
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

