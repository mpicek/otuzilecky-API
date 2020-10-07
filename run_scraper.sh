#!/usr/bin/env bash

set -ueo pipefail

git pull &> /dev/null

python3 malse_scraper.py
