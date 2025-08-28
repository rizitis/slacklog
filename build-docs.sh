#!/usr/bin/bash

cd doc || exit 1

sphinx-build -b html . _build/html
