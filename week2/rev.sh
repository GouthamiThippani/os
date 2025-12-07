#!/bin/bash

echo -n "Enter a number: "
read num

rev=0
temp=$num

while [ $temp -gt 0 ]
do
    digit=$((temp % 10))        # Get last digit
    rev=$((rev * 10 + digit))   # Add digit to reversed number
    temp=$((temp / 10))         # Remove last digit
done

echo "Reversed number: $rev"
