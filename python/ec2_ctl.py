# -*- coding: utf-8 -*-

""" Start, Stop, Restart EC2 (and more... later)

    Usage: ec2_ctl.py [EC2_Name_1 EC2_Name_2 ...] [start|stop|restart]
           ex: ec2_ctl.py Dev CDS stop

    Note:
        - venv를 PRD에서도 사용하기 때문에 보통 Python script 첫 라인에 적던
          #!/usr/bin/env python3 같은 shebang은 사용하지 않는다.

    References:
        https://serverfault.com/questions/560337/search-ec2-instance-by-its-name-from-aws-command-line-tool
        https://stackoverflow.com/questions/6289646/python-function-as-a-function-argument (function as argument)
        https://boto3.readthedocs.io/en/latest/guide/ec2-example-managing-instances.html
        https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_instances
"""
import click
import boto3
from botocore.exceptions import ClientError
from pprint import pprint


def start_stop(func, i_list):
    for i in i_list:
        try:
            func(InstanceIds=[i], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        try:
            res = func(InstanceIds=[i], DryRun=False)
            pprint(res)
        except ClientError as e:
            pprint(e)


@click.command()
# @click.option('--ex', is_flag=True, help='Exclude target on right')
@click.argument('target', nargs=-1)
@click.argument('command', type=click.Choice(['start', 'stop', 'restart']))
def run(target, command):
    ec2 = boto3.client('ec2')

    i_list = []
    for n in target:
        try:
            i_list.append(ec2.describe_instances(
                Filters=[{'Name': 'tag:Name', 'Values': [n]}])['Reservations'][0]['Instances'][0]['InstanceId'])
        except IndexError:
            print("Error: Check if instance name '%s' is correct." % n)
            exit(-1)

    if command == 'start':
        start_stop(ec2.start_instances, i_list)
    elif command == 'restart':
        start_stop(ec2.reboot_instances, i_list)
    else:  # 여기에는 stop만 오게 된다. 엉뚱한 값을 지정할 경우 Click이 Exception을 발생시킨다.
        start_stop(ec2.stop_instances, i_list)


if __name__ == "__main__":
    run()
