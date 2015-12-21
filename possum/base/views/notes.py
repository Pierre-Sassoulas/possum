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

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required

from possum.base.forms import NoteForm
from possum.base.models import Note
from possum.base.views import check_admin


LOGGER = logging.getLogger(__name__)


@login_required
def get_notes(request):
    context = {'menu_manager': True, }
    context['notes'] = Note.objects.all()
    return context


@user_passes_test(check_admin)
def home(request):
    context = get_notes(request)
    return render(request, 'notes/home.html', context)


@user_passes_test(check_admin)
def delete(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.delete()
    return redirect('notes_home')


@user_passes_test(check_admin)
def view(request, note_id=None):
    context = get_notes(request)
    if request.method == 'POST':
        if note_id:
            # note already exist
            note = get_object_or_404(Note, pk=note_id)
            context['note'] = NoteForm(request.POST, instance=note)
        else:
            # new note
            context['note'] = NoteForm(request.POST)
        if context['note'].is_valid():
            context['note'].save()
    else:
        if note_id:
            # note already exist
            note = get_object_or_404(Note, pk=note_id)
            context['note'] = NoteForm(instance=note)
        else:
            # new note
            context['note'] = NoteForm()
    return render(request, 'notes/home.html', context)
