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
from django.contrib.auth.models import User, UserManager
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test, login_required

from possum.base.views import check_admin, remove_edition


LOG = logging.getLogger(__name__)


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
        username = request.user.username
        if request.user.check_password(old):
            if new1 and new1 == new2:
                request.user.set_password(new1)
                request.user.save()
                messages.add_message(request, messages.SUCCESS,
                                     _("Password changed"))
                LOG.info('[%s] password changed' % username)
            else:
                messages.add_message(request, messages.ERROR,
                                     _("New password invalid"))
                LOG.warning('[%s] new password invalid' % username)
        else:
            messages.add_message(request, messages.ERROR,
                                 _("Invalid password"))
            LOG.warning('[%s] chk password failed' % username)
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
            LOG.info("[%s] new user [%s]" % (request.user.username, login))
        except:
            LOG.warning("[%s] new user failed: [%s] [%s] [%s] [%s]" % (
                        request.user.username, login, first_name, last_name,
                        mail))
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
        LOG.info("[%s] new login: [%s] > [%s]" % (request.user.username,
                                                  user.username, login))
        user.username = login
    if first_name != user.first_name:
        LOG.info("[%s] new first name for [%s]: [%s] > [%s]" % (
                 request.user.username, user.username, user.first_name,
                 first_name))
        user.first_name = first_name
    if last_name != user.last_name:
        LOG.info("[%s] new last name for [%s]: [%s] > [%s]" % (
                 request.user.username, user.username, user.last_name,
                 last_name))
        user.last_name = last_name
    if mail != user.email:
        LOG.info("[%s] new mail for [%s]: [%s] > [%s]" % (
                 request.user.username, user.username, user.email, mail))
        user.email = mail

    try:
        user.save()
    except:
        messages.add_message(request, messages.ERROR,
                             _("Changes could not be saved"))
        LOG.warning("[%s] save failed for [%s]" % (request.user.username,
                                                   user.username))
    return redirect('users')


@user_passes_test(check_admin)
def users_active(request, user_id):
    '''Enable ou disable users, we must have one at least.

    :param request: HttpRequest
    :param user_id: User pk
    '''
    user = get_object_or_404(User, pk=user_id)
    new = not user.is_active
    if not new and User.objects.filter(is_active=True).count() == 1:
        messages.add_message(request, messages.ERROR,
                             _("We must have at least one active user"))
        LOG.warning("[%s] we must have at least one active user")
    else:
        user.is_active = new
        user.save()
        LOG.info("[%s] user [%s] active: %s" % (request.user.username,
                                                user.username, user.is_active))
    return redirect('users')


@user_passes_test(check_admin)
def users_manager(request, user_id):
    """Set or unset admin rule for a user. You must have at least one admin.

    :param request: HttpResponse
    :param users_id: User pk
    """
    user = get_object_or_404(User, pk=user_id)
    new = not user.is_superuser
    if not new and User.objects.filter(is_active=True,
                                       is_superuser=True).count() == 1:
        messages.add_message(request, messages.ERROR,
                             _("We must have at least one active admin"))
        LOG.warning("[%s] we must have at least one active admin")
    else:
        user.is_superuser = new
        user.save()
        LOG.info("[%s] user [%s] admin: %s" % (request.user.username,
                                               user.username,
                                               user.is_superuser))
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
    LOG.info("[%s] user [%s] new password" % (request.user.username,
                                              user.username))
    return redirect('users')
