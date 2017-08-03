#!/usr/bin/env bash

project_path=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd ${project_path}

python test_article.py
