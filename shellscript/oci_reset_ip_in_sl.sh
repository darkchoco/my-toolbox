#!/usr/bin/bash

# DESCRIPTION:
#   OCI의 security list 내 IP 업데이트.
#   아래 명령을 사용해서 /home/$USER/dat/ 아래 ingress.json 이란 파일을 준비해놓아야 한다.
#   oci network security-list get --security-list-id <security-list-id> --query 'data."ingress-security-rules"' > /home/$USER/dat/ingress.json
#
# EXAMPLE:
#   ./oci_reset_ip_in_sl.sh
#
# REFERENCE:
#   https://docs.public.oneportal.content.oci.oraclecloud.com/en-us/iaas/tools/oci-cli/3.47.0/oci_cli_docs/cmdref/network/security-list/update.html

source ./env_oci_reset_ip_in_sl.sh

# 변수 설정
export default_display_name="Default Security List for prd-vcn"

# Security List ID 가져오기
security_list_id=$(oci network security-list list --compartment-id $compartment_id --vcn-id $vcn_id --query "data[?\"display-name\"=='$default_display_name'].id | [0]" --raw-output)

# Security List 업데이트
oci network security-list update --force --security-list-id $security_list_id --ingress-security-rules file:///home/$USER/dat/ingress.json
