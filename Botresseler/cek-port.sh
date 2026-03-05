#!/bin/bash
green="\e[32m"; red="\e[31m"; nc="\e[0m"
echo "🔍 CEK STATUS SERVER"
echo "===================="

vpn_servers=(
  "SG-1:sg1.domain.com"
  "SG-2:sg2.domain.com"
  "INDO-1:indo1.domain.com"
)

for server in "${vpn_servers[@]}"; do
  IFS=":" read -r name host <<< "$server"
  echo -e "\n🌐 $name"
  for port in 22 80 443; do
    timeout 2 bash -c "</dev/tcp/$host/$port" &>/dev/null
    if [[ $? -eq 0 ]]; then
      echo -e "  Port $port: ${green}OPEN${nc}"
    else
      echo -e "  Port $port: ${red}CLOSED${nc}"
    fi
  done
done
