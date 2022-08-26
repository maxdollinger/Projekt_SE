import enum

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect


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


def role_is_valid(request, role):
    user_role = get_user_role(request.user)
    if user_role == role:
        return True
    else:
        messages.error(request, "Du hast nicht die benötigten Berechtigungen für diese Funktion.")
        return False


def roles_are_valid(request, roles: list):
    is_valid = False
    user_role = get_user_role(request.user)

    for role in roles:
        if user_role == role:
            is_valid = True

    if is_valid:
        return True
    else:
        messages.error(request, "Du hast nicht die benötigten Berechtigungen für diese Funktion.")
        return False


class Roles(enum.Enum):
    STUDENT = 'Student'
    QM_LEADER = 'Leiter QM'
    IU_EMPLOYEE = 'Mitarbeiter IU'
    QM_MANAGER = 'Mitarbeiter QM'
