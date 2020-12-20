#!/bin/bash

FILES=$(find . -type f -name "*.py")

python -m pylint $FILES || pylint-exit $?
