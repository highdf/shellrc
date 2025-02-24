#! /bin/bash

limit=5
time=$((5 * 1))

while true; do
	capacity=$(cat /sys/class/power_supply/BAT0/capacity)
	if [[ ${capacity} -lt ${limit} ]]; then
		dunstify -u critical -h string:x-dunst-stack-tag:battery "bettery capacity is less than 5%"
	fi
	sleep ${time}
done
