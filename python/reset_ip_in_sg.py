# -*- coding: utf-8 -*-

""" Reset IP in Security Group with my local one

    Usage: reset_ip_in_sg.py TAG_NAME
           ex: reset_ip_in_sg.py HomeOffice

    Note:
        - Security Group Rule ID is used (introduced in July 2021). Boto3 version should be >= 1.8
        - 서버에서보다는 IP가 종종 바뀌는 집에서 유용하다.
        - venv를 PRD에서도 사용하기 때문에 보통 Python script 첫 라인에 적던
          #!/usr/bin/env python3 같은 shebang은 사용하지 않는다.

    References:
        - https://stackoverflow.com/questions/62592461/updating-existing-ips-from-a-security-group-in-aws-using-aws-cli
        - https://aws.amazon.com/blogs/aws/easily-manage-security-group-rules-with-the-new-security-group-rule-id/
        - https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
"""
import sys
import argparse
from requests import get
import boto3
from pprint import pprint


def parse_args(args):
    """Parse command line parameters
    https://docs.python.org/3/library/argparse.html
    """
    parser = argparse.ArgumentParser(
        description='Reset IP in Security Group with my local one - RUN IN LOCAL PC.')
    parser.add_argument(
        'tag_value',
        help='Value of Name=\'From\' in Tag assigned to SecurityGroupRuleId'
    )
    return parser.parse_args(args)


def main(args):
    args_ns = parse_args(args)

    ip = get('https://ident.me').text + "/32"

    ec2 = boto3.client('ec2')

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_group_rules
    res = ec2.describe_security_group_rules(
        Filters=[{'Name': 'tag:From',
                  'Values': [args_ns.tag_value]}])['SecurityGroupRules']
    # pprint(res)

    for sg in res:
        # print(sg['GroupId'], sg['SecurityGroupRuleId'])
        ret = ec2.revoke_security_group_ingress(GroupId=sg['GroupId'],
                                                SecurityGroupRuleIds=[sg['SecurityGroupRuleId']])
        if ret['Return']:
            print('Security Group Rule {} in Security Group {} deleted.\n'
                  .format(sg['SecurityGroupRuleId'], sg['GroupId']))
        else:
            print('Error in deleting Security Group Rule {} in Security Group {}. Check details.'
                  .format(sg['SecurityGroupRuleId'], sg['GroupId']))
            exit(-1)

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.authorize_security_group_ingress
        ret = ec2.authorize_security_group_ingress(
            GroupId=sg['GroupId'],
            IpPermissions=[
                {
                    'FromPort': sg['FromPort'],
                    'IpProtocol': 'tcp',
                    'IpRanges': [
                        {
                            'CidrIp': ip,
                            'Description': args_ns.tag_value
                        }
                    ],
                    'ToPort': sg['ToPort'],
                }
            ],
            TagSpecifications=[
                {
                    'ResourceType': 'security-group-rule',
                    'Tags': [
                        {
                            'Key': 'From',
                            'Value': args_ns.tag_value
                        }
                    ]
                }
            ]
        )

        if ret['Return']:
            print('New SecurityGroupRule added with tag value: \'{}\'.'.format(args_ns.tag_value))
            pprint(ret['SecurityGroupRules'])
            print('\n')
        else:
            print('Error in adding new Security Group Rule in Security Group {}. Check details.'
                  .format(sg['GroupId']))
            print('\n')
            exit(-1)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
