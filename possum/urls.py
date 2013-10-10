from django.conf.urls import patterns, include, url

# from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('possum.base.views',
    url(r'^$', 'home', name='home'),
#    (r'^accueil$', 'accueil'),

    url(r'^carte/$', 'categories'),
    url(r'^carte/print/$', 'categories_print'),
    url(r'^carte/send/$', 'categories_send'),
    url(r'^carte/categories/$', 'categories'),
    url(r'^carte/categories/add/$', 'categories_add'),
    url(r'^carte/categories/new/$', 'categories_new'),
    url(r'^carte/categories/(?P<cat_id>\d+)/$', 'categories_view'),
    url(r'^carte/categories/(?P<cat_id>\d+)/less/$', 'categories_less_priority'),
    url(r'^carte/categories/(?P<cat_id>\d+)/more/$', 'categories_more_priority'),
    url(r'^carte/categories/(?P<cat_id>\d+)/less-10/$', 'categories_less_priority', {'nb': 10}),
    url(r'^carte/categories/(?P<cat_id>\d+)/more-10/$', 'categories_more_priority', {'nb': 10}),
    url(r'^carte/categories/(?P<cat_id>\d+)/surtaxable/$', 'categories_surtaxable'),
    url(r'^carte/categories/(?P<cat_id>\d+)/name/$', 'categories_name'),
    url(r'^carte/categories/(?P<cat_id>\d+)/name/set/$', 'categories_set_name'),
    url(r'^carte/categories/(?P<cat_id>\d+)/color/$', 'categories_color'),
    url(r'^carte/categories/(?P<cat_id>\d+)/color/set/$', 'categories_set_color'),
    url(r'^carte/categories/(?P<cat_id>\d+)/vat_onsite/$', 'categories_vat_onsite'),
    url(r'^carte/categories/(?P<cat_id>\d+)/vat_onsite/set/(?P<vat_id>\d+)/$', 'categories_set_vat_onsite'),
    url(r'^carte/categories/(?P<cat_id>\d+)/vat_takeaway/$', 'categories_vat_takeaway'),
    url(r'^carte/categories/(?P<cat_id>\d+)/vat_takeaway/set/(?P<vat_id>\d+)/$', 'categories_set_vat_takeaway'),
    url(r'^carte/categories/(?P<cat_id>\d+)/delete/$', 'categories_delete'),
    url(r'^carte/categories/(?P<cat_id>\d+)/disable_surtaxe/$', 'categories_disable_surtaxe'),
    url(r'^carte/categories/(?P<cat_id>\d+)/kitchen/$', 'categories_set_kitchen'),
    url(r'^carte/categories/(?P<cat_id>\d+)/product/new/$', 'products_new'),

    url(r'^carte/products/(?P<product_id>\d+)/$', 'products_view'),
    url(r'^carte/products/(?P<product_id>\d+)/change/$', 'products_change'),
    url(r'^carte/products/(?P<product_id>\d+)/category/$', 'products_category'),
    url(r'^carte/products/(?P<product_id>\d+)/categories_ok/select/$', 'products_select_categories_ok'),
    url(r'^carte/products/(?P<product_id>\d+)/categories_ok/(?P<cat_id>\d+)/add/$', 'products_add_categories_ok'),
    url(r'^carte/products/(?P<product_id>\d+)/categories_ok/(?P<cat_id>\d+)/del/$', 'products_del_categories_ok'),
    url(r'^carte/products/(?P<product_id>\d+)/produits_ok/select/$', 'products_select_produits_ok'),
    url(r'^carte/products/(?P<product_id>\d+)/produits_ok/(?P<sub_id>\d+)/add/$', 'products_add_produits_ok'),
    url(r'^carte/products/(?P<product_id>\d+)/produits_ok/(?P<sub_id>\d+)/del/$', 'products_del_produits_ok'),
    url(r'^carte/products/(?P<product_id>\d+)/category/(?P<cat_id>\d+)/set/$', 'products_set_category'),
    url(r'^carte/products/(?P<product_id>\d+)/enable/$', 'products_enable'),
    url(r'^carte/products/(?P<product_id>\d+)/cooking/$', 'products_cooking'),

    url(r'^bills/$', 'factures'),
    url(r'^bill/new/$', 'bill_new'),
    url(r'^bill/(?P<bill_id>\d+)/table/select/$', 'table_select'),
    url(r'^bill/(?P<bill_id>\d+)/table/set/(?P<table_id>\d+)/$', 'table_set'),
    url(r'^bill/(?P<bill_id>\d+)/couverts/select/$', 'couverts_select'),
    url(r'^bill/(?P<bill_id>\d+)/couverts/set/(?P<number>\d+)/$', 'couverts_set'),
    url(r'^bill/(?P<bill_id>\d+)/category/select/$', 'category_select'),
    url(r'^bill/(?P<bill_id>\d+)/category/(?P<category_id>\d+)/$', 'category_select'),
    url(r'^bill/(?P<bill_id>\d+)/product/add/(?P<product_id>\d+)/$', 'product_add'),
    url(r'^bill/(?P<bill_id>\d+)/product/(?P<category_id>\d+)/select/$', 'product_select'),
    url(r'^bill/(?P<bill_id>\d+)/product/(?P<product_id>\d+)/made_with/$', 'product_select_made_with'),
    url(r'^bill/(?P<bill_id>\d+)/product/(?P<product_id>\d+)/made_with/(?P<category_id>\d+)/$', 'product_set_made_with'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<sold_id>\d+)/category/(?P<category_id>\d+)/select/$', 'subproduct_select'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<sold_id>\d+)/view/$', 'sold_view'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<menu_id>\d+)/(?P<sold_id>\d+)/cooking/$', 'sold_cooking'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<menu_id>\d+)/(?P<sold_id>\d+)/cooking/(?P<cooking_id>\d+)/$', 'sold_cooking'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<sold_id>\d+)/cooking/$', 'sold_cooking'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<sold_id>\d+)/cooking/(?P<cooking_id>\d+)/$', 'sold_cooking'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<sold_id>\d+)/delete/$', 'sold_delete'),
    url(r'^bill/(?P<bill_id>\d+)/sold/(?P<sold_id>\d+)/(?P<product_id>\d+)/add/$', 'subproduct_add'),
    url(r'^bill/(?P<bill_id>\d+)/delete/$', 'bill_delete'),
    url(r'^bill/(?P<bill_id>\d+)/onsite/$', 'bill_onsite'),
    url(r'^bill/(?P<bill_id>\d+)/payment/$', 'bill_payment'),
    url(r'^bill/(?P<bill_id>\d+)/payment/view/(?P<payment_id>\d+)/$', 'bill_payment_view'),
    url(r'^bill/(?P<bill_id>\d+)/payment/delete/(?P<payment_id>\d+)/$', 'bill_payment_delete'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/$', 'bill_payment'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/(?P<left>\d+).(?P<right>\d+)/(?P<count>\d+)/$', 'bill_payment'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/(?P<left>\d+).(?P<right>\d+)/(?P<count>\d+)/save/$', 'bill_payment_save'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/(?P<left>\d+).(?P<right>\d+)/(?P<count>\d+)/set/$', 'bill_payment_set'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/(?P<left>\d+).(?P<right>\d+)/(?P<count>\d+)/set/(?P<part>[a-z]{5})/$', 'bill_payment_set'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/(?P<left>\d+).(?P<right>\d+)/(?P<count>\d+)/set/left/(?P<number>\d)/$', 'bill_payment_set_left'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/(?P<left>\d+).(?P<right>\d+)/(?P<count>\d+)/set/right/(?P<number>\d)/$', 'bill_payment_set_right'),
    url(r'^bill/(?P<bill_id>\d+)/payment/(?P<type_id>\d+)/(?P<left>\d+).(?P<right>\d+)/count/$', 'bill_payment_count'),
    url(r'^bill/(?P<bill_id>\d+)/print/$', 'bill_print'),
    url(r'^bill/(?P<bill_id>\d+)/kitchen/$', 'bill_send_kitchen'),
    url(r'^bill/(?P<bill_id>\d+)/$', 'bill_view'),
    url(r'^jukebox/$', 'jukebox'),

    url(r'^kitchen/$', 'kitchen'),
    url(r'^kitchen/(?P<bill_id>\d+)/$', 'kitchen_for_bill'),

    url(r'^profile/$', 'profile'),

    url(r'^manager/$', 'manager'),
    url(r'^manager/credits/$', 'credits'),

    url(r'^manager/archives/$', 'archives'),
    url(r'^manager/archives/bill/(?P<bill_id>\d+)/$', 'archives_bill'),

    url(r'^manager/printers/$', 'printers'),
    url(r'^manager/printer/add/$', 'printer_add'),
    url(r'^manager/printer/add/(?P<name>[a-zA-Z0-9_-]+)/$', 'printer_added'),
    url(r'^manager/printer/(?P<printer_id>\d+)/$', 'printer_view'),
    url(r'^manager/printer/(?P<printer_id>\d+)/kitchen/$', 'printer_change_kitchen'),
    url(r'^manager/printer/(?P<printer_id>\d+)/billing/$', 'printer_change_billing'),
    url(r'^manager/printer/(?P<printer_id>\d+)/manager/$', 'printer_change_manager'),
    url(r'^manager/printer/(?P<printer_id>\d+)/width/$', 'printer_select_width'),
    url(r'^manager/printer/(?P<printer_id>\d+)/test/$', 'printer_test_print'),
    url(r'^manager/printer/(?P<printer_id>\d+)/width/set/(?P<number>\d+)/$', 'printer_set_width'),

    url(r'^manager/users/$', 'users'),
    url(r'^manager/users/new/$', 'users_new'),
    url(r'^manager/users/(?P<user_id>\d+)/passwd/$', 'users_passwd'),
    url(r'^manager/users/(?P<user_id>\d+)/active/$', 'users_active'),
    url(r'^manager/users/(?P<user_id>\d+)/change/$', 'users_change'),
    url(r'^manager/users/(?P<user_id>\d+)/perm/(?P<codename>p\d+)/$', 'users_change_perm'),

    url(r'^manager/vats/new/$', 'vat_new'),
    url(r'^manager/vats/$', 'vats'),
    url(r'^manager/vats/(?P<vat_id>\d+)/$', 'vats_view'),
    url(r'^manager/vats/(?P<vat_id>\d+)/change/$', 'vats_change'),

    url(r'^manager/tables/$', 'tables'),
    url(r'^manager/tables/new/$', 'tables_zone_new'),
    url(r'^manager/tables/(?P<zone_id>\d+)/$', 'tables_zone'),
    url(r'^manager/tables/(?P<zone_id>\d+)/new/$', 'tables_table_new'),
    url(r'^manager/tables/(?P<zone_id>\d+)/(?P<table_id>\d+)/$', 'tables_table'),
    url(r'^manager/tables/(?P<zone_id>\d+)/delete/$', 'tables_zone_delete'),

    url(r'^manager/rapports/$', 'rapports_daily'),
    url(r'^manager/rapports/daily/$', 'rapports_daily'),
    url(r'^manager/rapports/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/vats/print/$', 'rapports_daily_vats_print'),
    url(r'^manager/rapports/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/vats/send/$', 'rapports_daily_vats_send'),
    url(r'^manager/rapports/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/print/$', 'rapports_daily_print'),
    url(r'^manager/rapports/(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/send/$', 'rapports_daily_send'),
    url(r'^manager/rapports/weekly/$', 'rapports_weekly'),
    url(r'^manager/rapports/weekly/(?P<year>\d{4})/(?P<week>\d+)/vats/print/$', 'rapports_weekly_vats_print'),
    url(r'^manager/rapports/weekly/(?P<year>\d{4})/(?P<week>\d+)/vats/send/$', 'rapports_weekly_vats_send'),
    url(r'^manager/rapports/weekly/(?P<year>\d{4})/(?P<week>\d+)/print/$', 'rapports_weekly_print'),
    url(r'^manager/rapports/weekly/(?P<year>\d{4})/(?P<week>\d+)/send/$', 'rapports_weekly_send'),
    url(r'^manager/rapports/monthly/$', 'rapports_monthly'),
    url(r'^manager/rapports/monthly/(?P<year>\d{4})/(?P<month>\d+)/vats/print/$', 'rapports_monthly_vats_print'),
    url(r'^manager/rapports/monthly/(?P<year>\d{4})/(?P<month>\d+)/vats/send/$', 'rapports_monthly_vats_send'),
    url(r'^manager/rapports/monthly/(?P<year>\d{4})/(?P<month>\d+)/print/$', 'rapports_monthly_print'),
    url(r'^manager/rapports/monthly/(?P<year>\d{4})/(?P<month>\d+)/send/$', 'rapports_monthly_send'),

    url(r'^manager/graphics/year/(?P<choice>[a-zA-Z0-9_-]+)/$', 'graphics_year'),
)

urlpatterns += patterns('',
    url(r'^users/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^users/logout/$', 'django.contrib.auth.views.logout_then_login'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
