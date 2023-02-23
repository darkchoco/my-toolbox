#!/usr/bin/bash

# DESCRIPTION:
#   디렉토리 내 YYYYMMDD_HHMMSS.jpg 파일명의 시간을 1시간 뒤로 바꿔 Rename 하기.
#
# REFERENCE:
#   https://stackoverflow.com/questions/8899135/renaming-multiples-files-with-a-bash-loop

for i in *
do
	if [[ $i == *.sh ]]; then
		continue
	fi
	d=$(basename "$i" .JPG)
	pretty_date="${d:0:8} ${d:9:2}:${d:11:2}:${d:13:2}"
#    printf "%s" ${pretty_date}
	offset_mins=60
	start_unix=$(date -d "${pretty_date}" +%s)
	end_unix=$((start_unix + 60*offset_mins))
	end_date=$(date -d "@${end_unix}" '+%Y%m%d_%H%M%S')
#    echo "$end_date"
	mv -- "$i" "$end_date.JPG"
done
