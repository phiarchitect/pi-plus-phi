#!/usr/bin/env bash

rm splash.lst

for file in splash*.png
do
  echo file $file >> splash.lst
  echo duration 1 >> splash.lst
done

vim splash.lst
