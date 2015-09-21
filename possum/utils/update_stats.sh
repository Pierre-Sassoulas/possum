#!/bin/bash
pushd /opt/possum-software >/dev/null
source env/bin/activate
python ./manage.py update_stats
deactivate
popd >/dev/null
