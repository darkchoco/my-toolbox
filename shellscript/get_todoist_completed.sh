#!/usr/bin/bash

# DESCRIPTION:
#   Getting the list of completed tasks from Todoist.
#   crontab에 아래와 같이 등록해서 사용한다.
#
#   SHELL=/bin/bash
#   05 23 * * 0 /home/ubuntu/bin/get_todoist_completed.sh 2>&1
#
# EXAMPLE:
#   get_todoist_completed.sh
#
# REFERENCE:
#   https://www.baeldung.com/linux/bash-variables-export

source /home/ubuntu/bin/env.sh

curl https://api.todoist.com/sync/v9/completed/get_all \
  -H "Authorization: Bearer $todoist" \
  -d command='[
  {
    "since"=$(date -d "yesterday" '+%Y-%m-%d')T23:00:00.000000Z,
  }]' \
  | jq '.' \
  > /home/ubuntu/dat/completed_$(date '+%Y%m%d').json
