#!/bin/bash

# Set the log file location
log_file="~/keylog.log"

# Continuously log keyboard input
while true; do
  # Read the input from the keyboard
  input=$(cat /dev/stdin)

  # Append the input to the log file
  echo $input >> $log_file
done
