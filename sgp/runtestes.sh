#!/bin/bash
for file in $( ls --hide='*pyc' app/testes )
do
  echo ${file%%.*}
  python -m unittest app.testes.${file%%.*}

  # Do something else.
done
