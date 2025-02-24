#!/bin/bash

wallpaper_dir="$HOME/Pictures/screen"
time=$((60 * 10))

function random_switch() {
	local wall_paperarray=()
	local list=$(find "$1" -type f)

	while read file; do
		wall_paperarray+=("$file") 
	done <<< "${list}"

	# echo ${#wall_paperarray[@]}

	local random_index=$(( RANDOM % ${#wall_paperarray[@]}))
	wall_paper_file="${wall_paperarray[random_index]}"

	echo ${wall_paper_file}
	swww img -t random ${wall_paper_file}
	sed -i -e '/path = /{' -e 'c\' -e "    path = ${wall_paper_file}" -e '}' "$HOME/.config/hypr/hyprlock.conf"

	dunstify -a "WallPaper_Switch" "WallPaper_Switch successfully"
}

function choose() {
	local day=${DAY_START}
	local night=${DAY_END}
	local current_time=$(date +%k)

	if [[ ${current_time} -ge ${day} && ${current_time} -lt ${night} ]]; then
		echo "Light"
	else 
		echo "Night"
	fi
}

while true; do
	dir="${wallpaper_dir}/$(choose)"

	# echo "dir = ${dir}"

	if [[ !  -d $dir ]]; then
		echo "${dir} is not directory"
	fi

	random_switch ${dir}
	sleep ${time}
done
