#!/bin/bash
#
#  Assumes intial wd is the API project root.
#
#  Need to include the environment variables here or find another means of providing them.
#
#
cd ./sale_monitor/checker/
pipenv run python3.8 ./controller.py >> ../../log.txt 2>&1