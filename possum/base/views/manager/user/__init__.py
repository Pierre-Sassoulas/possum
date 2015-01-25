# -*- coding: utf-8 -*-
#
#    Copyright 2009-2014 Sébastien Bonnegent
#
#    This file is part of POSSUM.
#
#    POSSUM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    POSSUM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with POSSUM.  If not, see <http://www.gnu.org/licenses/>.
#

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, UserManager, Permission
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test, login_required

from possum.base.views import check_admin, remove_edition


LOGGER = logging.getLogger(__name__)


@login_required
def profile(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    request = remove_edition(request)
    context = {'menu_profile': True, }
    context['perms_list'] = settings.PERMS
    old = request.POST.get('old', '').strip()
    new1 = request.POST.get('new1', '').strip()
    new2 = request.POST.get('new2', '').strip()
    if old:
        if request.user.check_password(old):
            if new1 and new1 == new2:
                request.user.set_password(new1)
                request.user.save()
                messages.add_message(request, messages.SUCCESS,
                                     _("Password changed"))
                LOGGER.info('[%s] password changed' % request.user.username)
            else:
                messages.add_message(request, messages.ERROR,
                                     _("New password invalid"))
                LOGGER.warning('[%s] new password invalid' %
                               request.user.username)
        else:
            messages.add_message(request, messages.ERROR,
                                 _("Invalid password"))
            LOGGER.warning('[%s] chk password failed' % request.user.username)
    return render(request, 'base/profile.html', context)


@user_passes_test(check_admin)
def users(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    context = {'menu_manager': True, }
    context['perms_list'] = settings.PERMS
    context['users'] = User.objects.all()
    for user in context['users']:
        user.permissions = [p.codename for p in user.user_permissions.all()]
    return render(request, 'base/manager/users.html', context)


@user_passes_test(check_admin)
def users_new(request):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    '''
    login = request.POST.get('login', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    mail = request.POST.get('mail', '').strip()
    if login:
        user = User()
        user.username = login
        user.first_name = first_name
        user.last_name = last_name
        user.email = mail
        try:
            user.save()
            LOGGER.info("[%s] new user [%s]" % (request.user.username, login))
        except:
            LOGGER.warning("[%s] new user failed: [%s] [%s] [%s] [%s]" % (
                           request.user.username, login, first_name,
                           last_name, mail))
            messages.add_message(request, messages.ERROR,
                                 _("User creation failed"))
    return redirect('users')


@user_passes_test(check_admin)
def users_change(request, user_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param user_id:
    :type user_id:
    '''
    login = request.POST.get('login', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    mail = request.POST.get('mail', '').strip()
    user = get_object_or_404(User, pk=user_id)
    if login != user.username:
        LOGGER.info("[%s] new login: [%s] > [%s]" % (
                    request.user.username, user.username, login))
        user.username = login
    if first_name != user.first_name:
        LOGGER.info("[%s] new first name for [%s]: [%s] > [%s]" % (
                    request.user.username, user.username, user.first_name,
                    first_name))
        user.first_name = first_name
    if last_name != user.last_name:
        LOGGER.info("[%s] new last name for [%s]: [%s] > [%s]" % (
                    request.user.username, user.username, user.last_name,
                    last_name))
        user.last_name = last_name
    if mail != user.email:
        LOGGER.info("[%s] new mail for [%s]: [%s] > [%s]" % (
                    request.user.username, user.username, user.email, mail))
        user.email = mail

    try:
        user.save()
    except:
        messages.add_message(request, messages.ERROR,
                             _("Changes could not be saved"))
        LOGGER.warning("[%s] save failed for [%s]" % (request.user.username,
                                                      user.username))
    return redirect('users')


@user_passes_test(check_admin)
def users_active(request, user_id):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param user_id:
    :type user_id:
    '''
    user = get_object_or_404(User, pk=user_id)
    new = not user.is_active
    p1 = Permission.objects.get(codename="p1")
    if not new and \
            p1.user_set.count() == 1 and \
            p1 in user.user_permissions.all():
        messages.add_message(request, messages.ERROR,
                             _("We must have at least one active user with "
                               "P1 permission"))
        LOGGER.warning("[%s] we must have at least one active user "
                       "with P1 permission")
    else:
        user.is_active = new
        user.save()
        LOGGER.info("[%s] user [%s] active: %s" % (request.user.username,
                                                   user.username,
                                                   user.is_active))
    return redirect('users')


@user_passes_test(check_admin)
def users_passwd(request, user_id):
    ''' Set a new random password for a user.
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param user_id:
    :type user_id:
    '''
    user = get_object_or_404(User, pk=user_id)
    passwd = UserManager().make_random_password(length=10)
    user.set_password(passwd)
    user.save()
    messages.add_message(request, messages.SUCCESS,
                         "%s: %s" % (_("New password is"), passwd))
    LOGGER.info("[%s] user [%s] new password" % (request.user.username,
                                                 user.username))
    return redirect('users')


@user_passes_test(check_admin)
def users_change_perm(request, user_id, codename):
    '''
    :param HttpRequest request:
    :return rtype: HttpResponse
    :param user_id:
    :type user_id:
    :param codename:
    :type codename:
    '''
    user = get_object_or_404(User, pk=user_id)
    # little test because because user can do ugly things :)
    # now we are sure that it is a good permission
    if codename in settings.PERMS:
        perm = Permission.objects.get(codename=codename)
        if perm in user.user_permissions.all():
            if codename == 'p1' and perm.user_set.count() == 1:
                # we must have at least one person with this permission
                LOGGER.info("[%s] user [%s] perm [%s]: at least should have "
                            "one person" % (request.user.username,
                                            user.username,
                                            codename))
                messages.add_message(request, messages.ERROR,
                                     _("We must have at least one active user "
                                       "with P1 permission"))
            else:
                user.user_permissions.remove(perm)
                LOGGER.info("[%s] user [%s] remove perm: %s" % (
                            request.user.username,
                            user.username,
                            codename))
        else:
            user.user_permissions.add(perm)
            LOGGER.info("[%s] user [%s] add perm: %s" % (
                        request.user.username,
                        user.username,
                        codename))
    else:
        LOGGER.warning("[%s] wrong perm info: [%s]" % (request.user.username,
                                                       codename))
    return redirect('users')
