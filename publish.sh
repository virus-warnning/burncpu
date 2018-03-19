#!/bin/bash

python3 setup.py bdist_wheel
WHEEL=`find dist/* | tail -n 1`

if [ "$1" == "test" ]; then
  twine upload --repository testpypi ${WHEEL}
else
  twine upload ${WHEEL}
fi
