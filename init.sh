#!/bin/bash

pipenv sync
pipenv run flask --app sale_monitor init-db

#  This is the work around to python import system being total garbage.
ln ./sale_monitor/kroger/Communicator.py ./sale_monitor/checker/Communicator.py  # Sym link doesn't work.
cd ./sale_monitor/checker  # need this to avoid collateral damage
grep -rl 'Communicator' . | xargs sed -i 's%sale_monitor\.kroger\.Communicator%Communicator%'  #