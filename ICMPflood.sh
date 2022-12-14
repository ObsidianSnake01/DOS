#!/bin/bash

# Prompt the user for the target's IP address
read -p "Enter the target's IP address: " target_ip

# Set the spoofed source address
spoofed_source_address="192.168.1.5"

# Send spoofed ping packets to every computer on the network
ping -c 1 -S $spoofed_source_address $target_ip

# Use the nmap tool to scan the target network
nmap -sP $target_ip
