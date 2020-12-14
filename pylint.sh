#!/bin/bash

FILES=$(find . -type f -name "*.py")

python -m pylint $FILES

EXITCODE=$?

if [ $EXITCODE -le 4 ]; then
  # don't fail on Warnings
  exit 0
else
  exit $EXITCODE
fi
