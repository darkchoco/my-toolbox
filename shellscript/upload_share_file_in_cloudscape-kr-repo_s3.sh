#!/usr/bin/bash

# DESCRIPTION:
#   cloudscape-kr-repo S3에 일정시간 이후 expire 되도록 제한하여 파일 업로드
#
# EXAMPLE:
#   upload_share_file_in_cloudscape-kr-repo_s3 파일명 3600
#
# REFERENCE:
#   https://medium.com/@fullsour/how-to-share-file-easily-using-cli-with-s3-b0760a12de85

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 [file] [ExpireTime(sec)]"
    exit
fi

defaultExpireTime=3600

if [[ -n "$2" ]]; then
    defaultExpireTime=$2
fi

aws s3 cp "$1" s3://cloudscape-kr-repo/tmp/
aws s3 presign s3://cloudscape-kr-repo/tmp/"$1" --expires-in "$defaultExpireTime"
