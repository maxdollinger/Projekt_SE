from django.contrib.auth import get_user
from django.contrib.auth.models import User


def get_user_role(user):
    groups = user.groups.all().values_list('name', flat=True)
    if 'Leiter QM' in groups:
        return 'Leiter QM'
    if 'Mitarbeiter QM' in groups:
        return 'Mitarbeiter QM'
    if 'Mitarbeiter IU' in groups:
        return 'Mitarbeiter IU'
    if 'Student' in groups:
        return 'Student'


def get_assignee_users():
    users = {}
    for user in User.objects.all():
        role = get_user_role(user)
        if role is 'Mitarbeiter IU' or role is 'Mitarbeiter QM':
            users[user] = role

    return users


def get_qm_users():
    users = {}
    for user in User.objects.all():
        role = get_user_role(user)
        if role is 'Leiter QM' or role is 'Mitarbeiter QM':
            users[user] = role

    return users

