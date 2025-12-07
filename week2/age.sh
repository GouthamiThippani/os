#!/bin/bash
# Check age example

echo -n "Enter your age: "
read age

if [ $age -gt 18 ]; then
    echo "You are above 18."
elif [ $age -lt 18 ]; then
    echo "You are below 18."
else
    echo "You are exactly 18."
fi