#!/usr/bin/env bash

sudo chown -R ubuntu:ubuntu ~/Smart-Notes-Django
virtualenv /home/ubuntu/Smart-Notes-Django/myenv
source /home/ubuntu/Smart-Notes-Django/venv/bin/activate
pip install -r /home/ubuntu/Smart-Notes-Django/requirements.txt