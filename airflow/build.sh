#!/bin/bash
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
python3 -m build
pip3 uninstall -y airflow_auth
pip3 install ./dist/*.whl