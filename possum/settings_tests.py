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

from .common_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr'
DEFAULT_FROM_EMAIL = "noreply@example.org"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS += (
    'django_jenkins',
)

JENKINS_TASKS = (
    #    'django_jenkins.tasks.run_pylint',
    #    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.with_coverage',
    #    'django_jenkins.tasks.dir_tests',
    #    'django_jenkins.tasks.run_csslint',
    #    'django_jenkins.tasks.run_pyflakes',
)

COVERAGE_EXCLUDES_FOLDERS = ['possum/base/migrations/*',
                             'possum/stats/migrations/*', 'env/*']

# COVERAGE_REPORT_HTML_OUTPUT_DIR = 'reports/coverage.html/'
