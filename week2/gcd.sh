#!/bin/bash
# GCD using modulo method

echo -n "Enter first number: "
read a

echo -n "Enter second number: "
read b

while [ $b -ne 0 ]
do
    temp=$((a % b))   # remainder of a divided by b
    a=$b              # move b to a
    b=$temp           # move remainder to b
done

echo "GCD is: $a"
