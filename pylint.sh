#!/bin/bash

FILES=$(find . -type f -name "*.py")

python -m pylint $FILES

EXITCODE=$?

if [ $EXITCODE -eq 4 -o $EXITCODE -eq 12 ]; then
  # don't fail on Warnings, Refactorings
  echo "Overriding exit code $EXITCODE from pylint with 0"
  exit 0
else
  exit $EXITCODE
fi
