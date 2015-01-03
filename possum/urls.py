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

from django.conf import settings
from django.conf.urls import patterns, url, include

CAT_RGX = r'categorie/(?P<category_id>\d+)/'
VAT_RGX = r'vat/(?P<vat_id>\d+)/'
PRD_RGX = r'product/(?P<product_id>\d+)/'
OPT_RGX = r'option/(?P<option_id>\d+)/'
BIL_RGX = r'bill/(?P<bill_id>\d+)/'
SLD_RGX = r'sold/(?P<sold_id>\d+)/'
PRT_RGX = r'printer/(?P<printer_id>\d+)/'
USR_RGX = r'user/(?P<user_id>\d+)/'
NOT_RGX = r'note/(?P<note_id>\d+)/'
SUB_RGX = r'produits_ok/(?P<sub_id>\d+)/'
TAB_RGX = r'table/(?P<table_id>\d+)/'
COOK_RGX = r'cooking/(?P<cooking_id>\d+)/'
NB_RGX = r'(?P<number>\d+)/'
ZON_RGX = r'table/(?P<zone_id>\d+)/'

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
# Uncomment the next line to enable the admin:
# url(r'^admin/', include(admin.site.urls)),
urlpatterns = patterns('possum.base.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^shutdown/$', 'shutdown', name='shutdown'),
                       )

urlpatterns += patterns('', url(r'^stats/', include('possum.stats.urls')))

urlpatterns += patterns('possum.base.views.carte.categories',
                        url(r'^carte/$', 'categories',
                            name='home_categories'),
                        url(r'^carte/print/$', 'categories_print',
                            name='categories_print'),
                        url(r'^carte/send/$', 'categories_send',
                            name='categories_send'),
                        url(r'^carte/categories/$', 'categories',
                            name='categories'),
                        url(r'^carte/categories/add/$', 'categories_add',
                            name='categories_add'),
                        url(r'^carte/categories/new/$', 'categories_new',
                            name='categories_new'),
                        url(r'^carte/' + CAT_RGX + '$',
                            'categories_view',
                            name='categories_view'),
                        url(r'^carte/' + CAT_RGX + 'less/$',
                            'categories_less_priority',
                            name='categories_less_priority'),
                        url(r'^carte/' + CAT_RGX + 'more/$',
                            'categories_more_priority',
                            name='categories_more_priority'),
                        url(r'^carte/' + CAT_RGX + 'less-10/$',
                            'categories_less_priority', {'nb': 10},
                            name='categories_less_priority_10'),
                        url(r'^carte/' + CAT_RGX + 'more-10/$',
                            'categories_more_priority', {'nb': 10},
                            name='categories_more_priority_10'),
                        url(r'^carte/' + CAT_RGX + 'surtaxable/$',
                            'categories_surtaxable',
                            name='categories_surtaxable'),
                        url(r'^carte/' + CAT_RGX + 'name/$',
                            'categories_name',
                            name='categories_name'),
                        url(r'^carte/' + CAT_RGX + 'name/set/$',
                            'categories_set_name', name='categories_set_name'),
                        url(r'^carte/' + CAT_RGX + 'color/$',
                            'categories_color',
                            name='categories_color'),
                        url(r'^carte/' + CAT_RGX + 'color/set/$',
                            'categories_set_color',
                            name='categories_set_color'),
                        url(r'^carte/' + CAT_RGX + 'vat_onsite/$',
                            'categories_vat_onsite',
                            name='categories_vat_onsite'),
                        url(r'^carte/' + CAT_RGX + 'vat_takeaway/$',
                            'categories_vat_takeaway',
                            name='categories_vat_takeaway'),
                        url(r'^carte/' + CAT_RGX + 'set/' + VAT_RGX + '$',
                            'categories_set_vat', name='categories_set_vat'),
                        url(r'^carte/' + CAT_RGX + 'delete/$',
                            'categories_delete',
                            name='categories_delete'),
                        url(r'^carte/' + CAT_RGX + ''
                            r'disable_surtaxe/$',
                            'categories_disable_surtaxe',
                            name='categories_disable_surtaxe'),
                        url(r'^carte/' + CAT_RGX + 'kitchen/$',
                            'categories_set_kitchen',
                            name='categories_set_kitchen'),
                        )

urlpatterns += patterns('possum.base.views.carte',
                        url(r'^carte/' + CAT_RGX + 'product/new/$',
                            'products_new', name='products_new'),
                        url(r'^carte/' + PRD_RGX + '$', 'products_view',
                            name='products_view'),
                        url(r'^carte/' + PRD_RGX + OPT_RGX + '$',
                            'products_option', name='products_option'),
                        url(r'^carte/' + PRD_RGX + 'change/$',
                            'products_change', name='products_change'),
                        url(r'^carte/' + PRD_RGX + 'category/$',
                            'products_category', name='products_category'),
                        url(r'^carte/' + PRD_RGX + 'categories_ok/select/$',
                            'products_select_categories_ok',
                            name='products_select_categories_ok'),
                        url(r'^carte/' + PRD_RGX + 'categories_ok/' + CAT_RGX + 'add/$',
                            'products_add_categories_ok',
                            name='products_add_categories_ok'),
                        url(r'^carte/' + PRD_RGX + 'categories_ok/' + CAT_RGX + 'del/$',
                            'products_del_categories_ok',
                            name='products_del_categories_ok'),
                        url(r'^carte/' + PRD_RGX + 'produits_ok/select/$',
                            'products_select_produits_ok',
                            name='products_select_produits_ok'),
                        url(r'^carte/' + PRD_RGX + SUB_RGX + 'add/$',
                            'products_add_produits_ok',
                            name='products_add_produits_ok'),
                        url(r'^carte/' + PRD_RGX + SUB_RGX + 'del/$',
                            'products_del_produits_ok',
                            name='products_del_produits_ok'),
                        url(r'^carte/' + PRD_RGX + CAT_RGX + 'set/$',
                            'products_set_category',
                            name='products_set_category'),
                        url(r'^carte/' + PRD_RGX + 'enable/$',
                            'products_enable', name='products_enable'),
                        url(r'^carte/' + PRD_RGX + 'cooking/$',
                            'products_cooking', name='products_cooking'),
                        )


urlpatterns += patterns('possum.base.views.bill',
                        url(r'^bills/$', 'bill_home', name='bill_home'),
                        url(r'^bill/new/$', 'bill_new', name='bill_new'),
                        url(r'^' + BIL_RGX + 'table/select/$',
                            'table_select',
                            name='table_select'),
                        url(r'^' + BIL_RGX + 'set/' + TAB_RGX + '$', 'table_set',
                            name='table_set'),
                        url(r'^' + BIL_RGX + 'couverts/select/$',
                            'couverts_select',
                            name='couverts_select'),
                        url(r'^' + BIL_RGX + 'couverts/set/' + NB_RGX + '$',
                            'couverts_set', name='couverts_set'),
                        url(r'^' + BIL_RGX + 'categories/$',
                            'categories',
                            name='bill_categories'),
                        url(r'^' + BIL_RGX + CAT_RGX + '$',
                            'categories',
                            name='bill_categories'),
                        url(r'^' + BIL_RGX + 'number/(?P<count>\d+)/$',
                            'set_number',
                            name='bill_set_number'),
                        url(r'^' + BIL_RGX + 'product/add/' + PRD_RGX + '$',
                            'product_add', name='product_add'),
                        url(r'^' + BIL_RGX + 'product/' + CAT_RGX + 'select/$',
                            'product_select', name='product_select'),
                        url(r'^' + BIL_RGX + 'product/' + PRD_RGX + 'made_with/$',
                            'product_select_made_with',
                            name='product_select_made_with'),
                        url(r'^' + BIL_RGX + 'product/' + PRD_RGX + 'made_with/' + CAT_RGX + '$',
                            'product_set_made_with',
                            name='product_set_made_with'),
                        url(r'^' + BIL_RGX + SLD_RGX + CAT_RGX + 'select/$',
                            'subproduct_select', name='subproduct_select'),
                        url(r'^' + BIL_RGX + SLD_RGX + 'options/$',
                            'sold_options',
                            name='bill_sold_options'),
                        url(r'^' + BIL_RGX + SLD_RGX + 'working/$',
                            'sold_working',
                            name='bill_sold_working'),
                        url(r'^' + BIL_RGX + SLD_RGX + OPT_RGX + '$',
                            'sold_options',
                            name='bill_sold_options'),
                        url(r'^' + BIL_RGX + SLD_RGX + 'view/$',
                            'sold_view',
                            name='sold_view'),
                        url(r'^' + BIL_RGX + SLD_RGX + NOT_RGX + '$',
                            'sold_note',
                            name='sold_note'),
                        url(r'^' + BIL_RGX + SLD_RGX + OPT_RGX + '$',
                            'sold_option',
                            name='sold_option'),
                        url(r'^' + BIL_RGX + SLD_RGX + 'cooking/$',
                            'sold_cooking', name='sold_cooking'),
                        url(r'^' + BIL_RGX + SLD_RGX + COOK_RGX + '$',
                            'sold_cooking', name='sold_cooking'),
                        url(r'^' + BIL_RGX + SLD_RGX + 'delete/$',
                            'sold_delete', name='sold_delete'),
                        url(r'^' + BIL_RGX + SLD_RGX + PRD_RGX + 'add/$',
                            'subproduct_add', name='subproduct_add'),
                        url(r'^' + BIL_RGX + 'delete/$',
                            'bill_delete', name='bill_delete'),
                        url(r'^' + BIL_RGX + 'onsite/$',
                            'bill_onsite', name='bill_onsite'),
                        url(r'^' + BIL_RGX + 'payment/$',
                            'prepare_payment', name='prepare_payment'),
                        url(r'^' + BIL_RGX + 'payment/view/(?P<payment_id>\d+)/$',
                            'bill_payment_view', name='bill_payment_view'),
                        url(r'^' + BIL_RGX + 'payment/delete/(?P<payment_id>\d+)/$',
                            'bill_payment_delete', name='bill_payment_delete'),
                        url(r'^' + BIL_RGX + 'payment/type/(?P<type_id>\d+)/$',
                            'type_payment', name='type_payment'),
                        url(r'^' + BIL_RGX + 'payment/save/$',
                            'save_payment', name='save_payment'),
                        url(r'^' + BIL_RGX + 'payment/count/' + NB_RGX + '$',
                            'payment_count', name='payment_count'),
                        url(r'^' + BIL_RGX + 'print/$',
                            'bill_print', name='bill_print'),
                        url(r'^' + BIL_RGX + 'kitchen/$',
                            'bill_send_kitchen', name='bill_send_kitchen'),
                        url(r'^' + BIL_RGX + '$', 'bill_view',
                            name='bill_view'),
                        url(r'^amount/$',
                            'amount_payment',
                            name='amount_payment'),
                        url(r'^amount/del/$', 'amount_payment_del',
                            name='amount_payment_del'),
                        url(r'^amount/add/(?P<number>\d)/$',  # TOCHECK Regex for number different than NB_RGX
                            'amount_payment_add', name='amount_payment_add'),
                        url(r'^amount/right/$', 'amount_payment_right',
                            name='amount_payment_right'),
                        url(r'^amount/count/$',
                            'amount_count', name='amount_count'),
                        )

urlpatterns += patterns('possum.base.views.kitchen',
                        url(r'^kitchen/$', 'kitchen', name='kitchen'),
                        url(r'^kitchen/' + BIL_RGX + '$', 'kitchen_for_bill',
                            name='kitchen_for_bill'),
                        url(r'^follow/(?P<follow_id>\d+)/done/$',
                            'follow_done', name='follow_done'),
                        )

urlpatterns += patterns('possum.base.views.manager',
                        url(r'^manager/credits/$', 'credits', name='credits'),
                        url(r'^manager/check/$', 'check_new_version',
                            name='check_new_version'),
                        )

urlpatterns += patterns('possum.base.views.sales',
                        url(r'^sales/$', 'home', name='sales_home'),
                        )

urlpatterns += patterns('possum.base.views.editions',
                        url(r'^editions/$', 'editions_home',
                            name='editions_home'),
                        url(r'^editions/' + BIL_RGX + '$', 'editions_view',
                            name='editions_view'),
                        )


urlpatterns += patterns('possum.base.views.manager.archives',
                        url(r'^manager/archives/$', 'archives',
                            name='archives'),
                        url(r'^manager/archives/' + BIL_RGX + '$',
                            'archives_bill', name='archives_bill'),
                        )

urlpatterns += patterns('possum.base.views.manager.printers',
                        url(r'^printers/$', 'home', name='printer_home'),
                        url(r'^printers/add/$',
                            'printer_add', name='printer_add'),
                        url(r'^printers/add/(?P<name>[a-zA-Z0-9_-]+)/$',
                            'printer_added', name='printer_added'),
                        url(r'^' + PRT_RGX + '$',
                            'printer_view', name='printer_view'),
                        url(r'^' + PRT_RGX + 'kitchen/$',
                            'printer_change_kitchen',
                            name='printer_change_kitchen'),
                        url(r'^' + PRT_RGX + 'billing/$',
                            'printer_change_billing',
                            name='printer_change_billing'),
                        url(r'^' + PRT_RGX + 'manager/$',
                            'printer_change_manager',
                            name='printer_change_manager'),
                        url(r'^' + PRT_RGX + 'width/$',
                            'printer_select_width', name='printer_select_width'),
                        url(r'^' + PRT_RGX + 'test/$',
                            'printer_test_print', name='printer_test_print'),
                        url(r'^' + PRT_RGX + 'width/set/' + NB_RGX + '$',
                            'printer_set_width', name='printer_set_width'),
                        url(r'^' + PRT_RGX + 'kitchen_header/$',
                            'kitchen_header', name='printer_kitchen_header'),
                        url(r'^' + PRT_RGX + 'kitchen_header/' + NB_RGX + '$',
                            'kitchen_header', name='printer_kitchen_header'),
                        )

urlpatterns += patterns('possum.base.views.manager.user',
                        url(r'^profile/$', 'profile', name='profile'),
                        url(r'^manager/users/$', 'users', name='users'),
                        url(r'^manager/users/new/$',
                            'users_new', name='users_new'),
                        url(r'^manager/' + USR_RGX + 'passwd/$',
                            'users_passwd', name='users_passwd'),
                        url(r'^manager/' + USR_RGX + 'active/$',
                            'users_active', name='users_active'),
                        url(r'^manager/' + USR_RGX + 'change/$',
                            'users_change', name='users_change'),
                        url(r'^manager/' + USR_RGX + 'perm/(?P<codename>p\d+)/$',
                            'users_change_perm', name='users_change_perm'),
                        )

urlpatterns += patterns('',
                        url(r'^users/login/$',
                            'django.contrib.auth.views.login',
                            {'template_name': 'login.html'}, name="login"),
                        url(r'^users/logout/$',
                            'django.contrib.auth.views.logout_then_login',
                            name="logout"),
                        )

urlpatterns += patterns('possum.base.views.manager.vats',
                        url(r'^manager/vats/new/$', 'vat_new', name='vat_new'),
                        url(r'^manager/vats/$', 'vats', name='vats'),
                        url(r'^manager/' + VAT_RGX + '$',
                            'vats_view', name='vats_view'),
                        url(r'^manager/' + VAT_RGX + 'change/$',
                            'vats_change', name='vats_change'),
                        )

urlpatterns += patterns('possum.base.views.manager.tables',
                        url(r'^manager/tables/$', 'tables', name='tables'),
                        url(r'^manager/tables/new/$',
                            'tables_zone_new', name='tables_zone_new'),
                        url(r'^manager/' + ZON_RGX + '$',
                            'tables_zone', name='tables_zone'),
                        url(r'^manager/' + ZON_RGX + 'new/$',
                            'tables_table_new', name='tables_table_new'),
                        url(r'^manager/' + ZON_RGX + TAB_RGX + '$',
                            'tables_table', name='tables_table'),
                        url(r'^manager/' + ZON_RGX + 'delete/$',
                            'tables_zone_delete', name='tables_zone_delete'),
                        )

urlpatterns += patterns('possum.base.views.notes',
                        url(r'^notes/$', 'home', name='notes_home'),
                        url(r'^notes/add/$', 'view', name='notes_add'),
                        url(r'^' + NOT_RGX + '$',
                            'view', name='notes_view'),
                        url(r'^' + NOT_RGX + 'del/$',
                            'delete', name='notes_del'),
                        )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT},
                                name="django_serve"),
                            )

urlpatterns += patterns('', url(r'^jukebox/', include('possum.jukebox.urls')),)

#    import debug_toolbar
#    urlpatterns += patterns('',
#        url(r'^__debug__/', include(debug_toolbar.urls)),
#    )
