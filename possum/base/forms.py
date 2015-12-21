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

from datetime import datetime
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext as _

from possum.base.models import Facture, Note, Option


LOGGER = logging.getLogger(__name__)


try:
    first_year = Facture.objects.first().date_creation.year
    last_year = Facture.objects.last().date_creation.year + 1
except:
    LOGGER.debug("no Facture, we keep default data")
    first_year = int(datetime.now().year)
    last_year = first_year + 1

years_list = [i for i in range(first_year, last_year)]


class DateForm(forms.Form):
    """Form permitting to choose a date.
    """
    date = forms.DateField(widget=SelectDateWidget(years=years_list))


class LoginForm(forms.Form):
    """Class LoginForm representing a form to log an User in.
    """
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'identifiant:'}))
    password = forms.CharField(widget=forms.PasswordInput(
                               attrs={'placeholder': 'mot de passe:'}))


class NoteForm(forms.ModelForm):
    """Form to edit a note
    """
    class Meta:
        model = Note
        fields = "__all__"
        widgets = {'message': forms.TextInput(attrs={
            'placeholder': _('New note'),
            'class': "form-control"})}


class OptionForm(forms.ModelForm):
    """Form to edit an option
    """
    class Meta:
        model = Option
        fields = "__all__"
