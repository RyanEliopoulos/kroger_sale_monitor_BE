#!/bin/bash

pipenv sync
pipenv run flask --app sale_monitor init-db