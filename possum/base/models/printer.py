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
import os
import unicodedata

from django.conf import settings
from django.db import models


LOGGER = logging.getLogger(__name__)


try:
    import cups
except Exception as err:
    LOGGER.critical("Printer library encountered an error :\n{0}".format(err))


def sans_accent(message):
    """Removes accents that may pose printing problem"""
    normalize = unicodedata.normalize("NFKD", unicode(message))
    return normalize.encode("ascii", "ignore")


class Printer(models.Model):
    """Printer model
    :param options: options used with pycups.printFile()
    :param header: you can add a text before the text to print (restaurant
    name)
    :param width: width of the ticket
    :param footer: same as header but after :)
    :param kitchen_lines: number of white lines to heading ticket of kitchen
    :param kitchen: used to print in kitchen
    :param billing: used to print bills
    :param manager: used to print rapport, ...
    """
    name = models.CharField(max_length=40)
    options = models.CharField(max_length=120)
    header = models.TextField(default="")
    footer = models.TextField(default="")
    width = models.PositiveIntegerField(default=27)
    kitchen_lines = models.IntegerField(default=0)
    kitchen = models.BooleanField(default=False)
    billing = models.BooleanField(default=False)
    manager = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_resume(self):
        """
        Useful to have a brief resume:
        :return: A character in [K,B,M] K : kitchen, B : billing, M : manager
        """
        if self.kitchen:
            return "K"
        if self.billing:
            return "B"
        if self.manager:
            return "M"
        return ""

    def get_available_printers(self):
        """
        :return: A string list of available printers
        """
        result = []
        try:
            conn = cups.Connection()
        except RuntimeError:
            return result
        printers = conn.getPrinters()
        for printer in printers:
            if Printer.objects.filter(name=printer).count() == 0:
                result.append(printer)
        return result

    def print_file(self, filename):
        '''
        TODO Docstring
        :param filename:
        :return: Boolean
        '''
        if not os.path.exists(filename):
            return False
        title = filename.split("/")[-1]
        try:
            conn = cups.Connection()
            conn.printFile(self.name, filename, title=title, options={})
            return True
        except:
            return False

    def print_msg(self, msg):
        ''' Try to print a message, we create a list with message

        :param String msg: A message to print
        :return: TODO
        '''
        list_to_print = msg.split("\n")
        return self.print_list(list_to_print, "possum")

    def print_list(self, list_to_print, name, with_header=False,
                   kitchen=False):
        ''' Generate a print list from a list which contains informations
        in string and several business objects.

        :param list_to_print: TODO
        :type list_to_print:
        :param name: TODO
        :type name:
        :param Boolean with_header:
        :param Boolean kitchen:
        '''
        path = "{0}/{1}-{2}.txt".format(settings.PATH_TICKET, self.id, name)
        ticket_to_print = open(path, "w")
        if kitchen and self.kitchen_lines:
            ticket_to_print.write("\n" * self.kitchen_lines)
        if with_header:
            ticket_to_print.write(self.header)
        for line in list_to_print:
            ticket_to_print.write("{0}\n".format(sans_accent(line)))
        if with_header:
            ticket_to_print.write(self.footer)
        ticket_to_print.close()
        result = self.print_file(path)
        os.remove(path)
        return result

    def print_test(self):
        '''
        Test the printer.
        '''
        list_to_print = []
        list_to_print.append("> POSSUM Printing test !")
        list_to_print.append(datetime.now().strftime("> %H:%M %d/%m/%Y\n"))
        return self.print_list(list_to_print, "test")
