#!/bin/bash
JQUERY="jquery-2.1.3.min.js"
HIGHCHARTS="Highcharts-3.0.6.zip"
HIGHDIR=${HIGHCHARTS/.zip/}
BOOTSTRAP_VERSION="3.3.4"
BOOTSTRAP="bootstrap-${BOOTSTRAP_VERSION}-dist.zip"
BOOTDIR=${BOOTSTRAP/.zip/}
DATEPICKER_VERSION="1.3.1"
STATIC="possum/base/static/"
APPS="base stats"

function my_help {
    cat << 'EOF'

Usage: ./make [a command]

List of commands:
    create_json_demo   :  create JSON fixtures in
                          possum/base/fixtures/demo.json
    doc                :  make the documentation in html
    deb_install_nginx  :  install nginx on Debian/Ubuntu (*)
    help               :  this help
    init_demo          :  erase database with data of demonstration (Warning
                          it can be very long in particular after 'Running
                          migrations')
    init_mine          :  run possum/utils/init_mine.py in virtualenv
    load_demo          :  load database with data of demonstration
    migrations         :  prepare files after modified models
    sh                 :  run ./manage.py shell_plus in virtualenv
    run                :  run ./manage.py runserver in virtualenv with the
                          file settings.py
    translation        :  create/update translations
    tests              :  make tests and coverage
    update             :  install/update Possum environnement

Note: If you need to define a proxy, set $http_proxy.
Example:
    export http_proxy="http://proxy.possum-software.org:8080/"
    export https_proxy="https://proxy.possum-software.org:8080/"

Note2: (*) must be root to do it

EOF
    exit 1
}

function enter_virtualenv {
    if [ ! -d env ]
    then
        update
    fi
    source env/bin/activate 2>/dev/null
    if [ ! $? -eq 0 ]
    then
        echo
        echo "Virtualenv does not work !"
        echo
        exit 2
    fi
}

function doc {
    enter_virtualenv
    for translation in en fr
    do
        pushd docs/$translation
        make html
        popd
    done
}

function create_json_demo {
    enter_virtualenv
    ./manage.py dumpdata --format=json --indent=4 --exclude=contenttypes --exclude=auth.Permission > possum/base/fixtures/demo.json
}

function tests {
    enter_virtualenv
    if [ ! -d reports ]
    then
        mkdir reports
    fi
    ./manage.py validate_templates --settings=possum.settings_tests
    if [ ! $? == 0 ]
    then
        exit $?
    fi
    flake8 --exclude=migrations --max-complexity 12 possum > reports/flake8.report
    sloccount --details possum > reports/soccount.sc
    coverage run --source='.' ./manage.py test --settings=possum.settings_tests
    RETOUR=$?
    coverage xml -o reports/coverage.xml
    exit $RETOUR
}

function update_js {
    # update javascript part
    # JQuery
    if [ ! -e ${STATIC}${JQUERY} ]
    then
        echo "Download and install JQuery..."
        wget http://code.jquery.com/${JQUERY} -O ${STATIC}${JQUERY}
    fi
    # Highcharts
    if [ ! -e ${STATIC}${HIGHCHARTS} ]
    then
        echo "Download HighCharts..."
        wget http://code.highcharts.com/zips/${HIGHCHARTS} -O ${STATIC}${HIGHCHARTS}
    fi
    if [ ! -e ${STATIC}${HIGHDIR} ]
    then
        mkdir ${STATIC}${HIGHDIR}
        echo "Unzip HighCharts..."
        pushd ${STATIC}${HIGHDIR} >/dev/null
        unzip ../${HIGHCHARTS}
        popd >/dev/null
    fi
    # BootStrap
    if [ ! -e ${STATIC}${BOOTSTRAP} ]
    then
        echo "Download BootStrap..."
        wget https://github.com/twbs/bootstrap/releases/download/v${BOOTSTRAP_VERSION}/${BOOTSTRAP} \
            -O ${STATIC}${BOOTSTRAP}
    fi
    if [ ! -e ${STATIC}${BOOTDIR} ]
    then
        echo "Unzip BootStrap..."
        pushd ${STATIC} >/dev/null
        unzip ${BOOTSTRAP}
        if [ ! -e ${STATIC}fonts ]
        then
            mkdir ${STATIC}fonts
        fi
        cp -f ${BOOTDIR}/fonts/* fonts/
        popd >/dev/null
    fi
    # BootStrap Date-Picker
    if [ ! -e ${STATIC}${DATEPICKER_VERSION}.zip ]
    then
        echo "Download BootStrap Date-Picker..."
        wget https://github.com/eternicode/bootstrap-datepicker/archive/${DATEPICKER_VERSION}.zip \
            -O ${STATIC}bootstrap-datepicker-${DATEPICKER_VERSION}.zip
    fi
    if [ ! -e ${STATIC}bootstrap-datepicker-${DATEPICKER_VERSION} ]
    then
        echo "Unzip BootStrap Date-Picker..."
        pushd $STATIC >/dev/null
        unzip bootstrap-datepicker-${DATEPICKER_VERSION}.zip
#        for dir in js css
#        do
#            if [ -e ${dir} ]
#            then
#                # old version
#                rm -rf ${dir}
#            fi
#            cp -a bootstrap-datepicker-${DATEPICKER_VERSION}/${dir} ${dir}
#        done
        popd >/dev/null
    fi
    enter_virtualenv
    ./manage.py collectstatic --noinput --no-post-process
}

function update {
#    chmod 755 possum/static/
    if [ ! -d env ]
    then
        echo
        echo "Host must be connected to Internet for this step."
        echo "And you must have some packages installed:"
        echo "You must read documentation :)"
        echo
        # For the moment, we stay with python2.
        virtualenv --python=python2 env
    fi
    enter_virtualenv
    # before all, we must have last release of Django
    pip install --upgrade --proxy=${http_proxy} $(grep -i django requirements.txt)
    pip install --proxy=${http_proxy} --requirement requirements.txt --upgrade
    if [ $? != 0 ]
    then
        echo "ERROR: pip failed !"
        exit 2
    fi
    # cleanup all .pyc files in possum
    find possum -name "*.pyc" -exec rm -f {} \;
    if [ ! -e possum/settings.py ]
    then
        # default conf is production
        cp possum/settings_production.py possum/settings.py
        ./manage.py migrate --noinput
        ./manage.py init_db
        cat << 'EOF'
-------------------------------------------------------
To use Possum, copy and adapt possum/base/management/commands/init_db.py.

Example:
  cp possum/base/management/commands/init_db.py possum/base/management/commands/init_mine.py
  # adapt possum/base/management/commands/init_mine.py file
  # and execute it
  ./make init_mine
-------------------------------------------------------
EOF
    fi
    ./manage.py migrate
    ./manage.py update_css
    ./manage.py update_stats_to_0_6
    update_js
}

function deb_install_nginx {
    sudo apt-get install nginx-light supervisor
    echo
    echo "Config example for Supervisor: possum/utils/supervisor.conf"
    echo "  cp possum/utils/supervisor.conf /etc/supervisor/conf.d/possum.conf"
    echo "  /etc/init.d/supervisor restart"
    echo
    echo "Config example for NGinx: possum/utils/nginx-ssl.conf"
    echo "  cp possum/utils/nginx-ssl.conf /etc/nginx/sites-enabled/default"
    echo "  /etc/init.d/nginx restart"
    echo
}

function graph_models {
    enter_virtualenv
    for app in $APPS
    do
        ./manage.py graph_models --output=docs/images/models-${app}.png -g ${app}
        echo "[docs/images/models-${app}.png] updated"
    done
}

function clear_db {
    enter_virtualenv
    ./manage.py reset_db
    ./manage.py migrate --noinput
#    ./manage.py flush --noinput
}

if [ ! $# -eq 1 ]
then
    my_help
fi

case "$1" in
create_json_demo)
    create_json_demo
    ;;
init_mine)
    enter_virtualenv
    clear_db
    possum/utils/init_mine.py
    ;;
init_demo)
    enter_virtualenv
    clear_db
    ./manage.py init_demo
    ;;
load_demo)
    enter_virtualenv
    clear_db
    ./manage.py migrate --noinput
    ./manage.py loaddata demo
    ;;
deb_install_nginx)
    deb_install_nginx
    ;;
doc)
    doc
    ;;
update)
    update
    ;;
migrations)
    enter_virtualenv
    for app in $APPS
    do
        ./manage.py makemigrations ${app}
    done
    ./manage.py migrate
    clear_db
    ./manage.py init_demo
    create_json_demo
    graph_models
    ;;
tests)
    tests
    ;;
sh)
    enter_virtualenv
    ./manage.py shell_plus
    ;;
run)
    enter_virtualenv
    ./manage.py runserver --settings=possum.settings
    ;;
translation)
    enter_virtualenv
    ./manage.py makemessages -i env --no-obsolete -l fr -l en -l ru
    ./manage.py compilemessages
    ;;
*)
    my_help
    ;;
esac

