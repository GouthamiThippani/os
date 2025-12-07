#!/bin/bash
# Sum of series 1+2+...+n

echo -n "Enter n: "
read n

sum=0
for (( i=1; i<=n; i++ ))
do
    sum=$((sum + i))
done

echo "Sum of series = $sum"