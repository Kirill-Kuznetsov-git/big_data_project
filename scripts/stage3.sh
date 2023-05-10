#!/bin/bash

rm -rf output/q1
rm -rf output/q2
rm -rf output/q3
rm -rf output/q4
rm -rf output/q5
rm -rf output/q6
rm -rf output/q7

python3 scripts/EDA.py

python3 scripts/PDA.py