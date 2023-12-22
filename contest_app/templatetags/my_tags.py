from django import template
from django.db.models import Count

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


