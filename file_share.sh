#!/bin/bash

# Prompt the user for the target file
read -p "Enter the target file: " target

# Prompt the user for the file to be sent
read -p "Enter the file to send: " file

# Send the file to the target
scp "$file" "$target"

# Check if the file was successfully sent
if [ $? -eq 0 ]; then
  # Hide the file being sent
  chmod -x "$file"

  # Disguise the user as Google
  export PS1="[google.com] $PS1"

  # Send the target multiple decoy IPs
  for i in {1..10}
  do
    decoy_ip="192.0.2.$i"
    echo "$decoy_ip" >> "$target"
  done

  # Print "done"
  echo "done"
else
  # Print an error message
  echo "Failed to send file"
fi
