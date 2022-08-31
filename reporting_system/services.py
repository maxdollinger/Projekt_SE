from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from enum import Enum
import os


def get_user_role(user):
    groups = user.groups.all().values_list('name', flat=True)

    if Roles.QM_LEADER.value in groups:
        return Roles.QM_LEADER.value
    if Roles.QM_MANAGER.value in groups:
        return Roles.QM_MANAGER.value
    if Roles.IU_EMPLOYEE.value in groups:
        return Roles.IU_EMPLOYEE.value
    if Roles.STUDENT.value in groups:
        return Roles.STUDENT.value


def get_assignee_users():
    users = {}
    for user in User.objects.all():
        role = get_user_role(user)
        if role == Roles.IU_EMPLOYEE.value or role == Roles.QM_MANAGER.value:
            users[user] = role

    return users


def get_qm_users():
    users = {}
    for user in User.objects.all():
        role = get_user_role(user)
        if role == Roles.QM_LEADER.value or role == Roles.QM_MANAGER.value:
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


class Roles(Enum):
    STUDENT = 'Student'
    QM_LEADER = 'Leiter QM'
    IU_EMPLOYEE = 'Mitarbeiter IU'
    QM_MANAGER = 'Mitarbeiter QM'


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
