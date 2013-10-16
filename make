#!/bin/bash
JQUERY="jquery-2.0.3.min.js"
HIGHCHARTS="Highcharts-3.0.6.zip"

function my_help {
    cat << 'EOF'

Usage: ./make [a command]

List of commands:
    doc            :  make the documentation in html
    help           :  this help
    install_debian :  install required packages on Debian/Ubuntu
    init_demo      :  erase database with data of demonstration
    init_mine      :  run possum/utils/init_mine.py in virtualenv 
    model          :  generate doc/images/models-base.png
    sh             :  run ./manage.py shell_plus in virtualenv
    run            :  run ./manage.py runserver_plus in virtualenv
    tests          :  make tests and coverage
    update         :  install/update Possum environnement

Note: If you need to define a proxy, set $http_proxy.
Example: export http_proxy="http://proxy.possum-software.org:8080/"

EOF
    exit 1
}

function enter_virtualenv {
    source .virtualenv/bin/activate 2>/dev/null
    if [ ! $? -eq 0 ]
    then
        echo
        echo "Virtualenv does not exist, run: $0 update"
        echo
        exit 2
    fi
}

function doc {
    enter_virtualenv
    cd doc
    make html
    echo "Documentation is in: doc/_build/html/"
}

function tests {
    enter_virtualenv
    OMIT="django_extensions,django,*migrations*,*.virtualenv*"
    coverage run --source=. manage.py test --verbosity=2 --traceback
    coverage report --omit=${OMIT}
    coverage html --omit=${OMIT}
    coverage xml --omit=${OMIT}
}

function update_js {
    # update javascript part
    if [ ! -e possum/static/jquery.min.js ]
    then
        echo "Download and install JQuery..."
        wget http://code.jquery.com/${JQUERY} -O possum/static/jquery.min.js
    fi

    if [ ! -d possum/static/highcharts ]
    then
        mkdir -v possum/static/highcharts
    fi
    if [ ! -e possum/static/highcharts/${HIGHCHARTS} ]
    then
        echo "Download HighCharts..."
        wget http://code.highcharts.com/zips/${HIGHCHARTS} -O possum/static/highcharts/${HIGHCHARTS}
    fi
    if [ ! -e possum/static/highcharts/js/highcharts.js ]
    then
        echo "Unzip HighCharts..."
        pushd possum/static/highcharts/ >/dev/null
        unzip Highcharts-3.0.6.zip
        popd >/dev/null
    fi

    if [ ! -d possum/static/chartit ]
    then
        mkdir -pv possum/static/chartit/js
    fi
    if [ ! -d possum/static/chartit/js ]
    then
        mkdir -pv possum/static/chartit/js
    fi
    if [ ! -e possum/static/chartit/js/chartloader.js ]
    then
        find .virtualenv/ -name chartloader.js -exec cp {} possum/static/chartit/js/chartloader.js \;
    fi
}

function update {
    echo
    echo "Host must be connected to Internet for this step."
    echo "And you must have some packages installed:"
    echo "Debian/Ubuntu> ./make install_debian"
    echo
    if [ ! -d .virtualenv ]
    then
        # For the moment, we stay with python2.
        virtualenv --prompt=="POSSUM" --python=python2 .virtualenv
    fi
    enter_virtualenv
    pip install --proxy=${http_proxy} --requirement requirements.txt
    update_js
    if [ ! -e possum/settings.py ]
    then
        # default conf is production
        cp possum/settings_production.py possum/settings.py
        ./manage.py syncdb --noinput --migrate
        possum/utils/init_db.py
        cat << 'EOF'
-------------------------------------------------------
To use Possum, copy and adapt possum/utils/init_db.py.

Example:
  cp possum/utils/init_db.py possum/utils/init_mine.py
  # adapt possum/utils/init_yours.py file
  # and execute it
  ./make init_mine
-------------------------------------------------------
EOF
    fi
    ./manage.py migrate base
}

function install_debian {
    echo
    echo "You must be Root to install, if fail try with sudo:"
    echo
    apt-get install graphviz-dev graphviz libcups2-dev memcached \
        python-virtualenv apache2 libapache2-mod-wsgi unzip \
        pkg-config python-dev cups-client cups
    a2dismod status cgid autoindex
    a2enmod wsgi ssl
}

if [ ! $# -eq 1 ]
then
    my_help
fi

case "$1" in
init_mine)
    enter_virtualenv
    possum/utils/init_mine.py
    ;;
init_demo)
    enter_virtualenv
    possum/utils/init_demo.py
    ;;
install_debian)
    install_debian
    ;;
doc)
    doc
    ;;
model)
    enter_virtualenv
    ./manage.py graph_models --output=doc/images/models-base.png -g base
    echo "[doc/images/models-base.png] updated"
    ;;
update)
    update
    ;;
tests)
    update
    tests
    doc
    ;;
sh)
    enter_virtualenv
    ./manage.py shell_plus
    ;;
run)
    enter_virtualenv
    ./manage.py runserver_plus
    ;;
*)
    my_help
    ;;
esac