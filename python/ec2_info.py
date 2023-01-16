# -*- coding: utf-8 -*-

""" EC2 info

    Usage: ec2_info.py [all|on|off]
           ex: ec2_info.py -all

    Description:
      - EC2 instance의 현재 상태를 보여준다. (Name, InstanceId, PrivIp, PubIp)

    Note:
        - venv를 PRD에서도 사용하기 때문에 보통 Python script 첫 라인에 적던
          #!/usr/bin/env python3 같은 shebang은 사용하지 않는다.

    References:
      - http://click.pocoo.org/5/options/#feature-switches
"""
import click
import boto3
import prettytable


@click.command()
@click.option('--all', 'target', flag_value='all', default=True, help='All EC2 info')
@click.option('--on', 'target', flag_value='running', help='All running EC2 info')
@click.option('--off', 'target', flag_value='stopped', help='All not-running EC2 info')
def run(target):
    ec2 = boto3.client('ec2')

    ec2_list = []
    res = ec2.describe_instances()
    for i in res['Reservations']:  # list of instance (dictionary type)
        if target == 'all':
            ec2_list.append(i)
            # print(i['Instances'][0]['InstanceId'])
        else:
            if i['Instances'][0]['State']['Name'] == target:
                ec2_list.append(i)
                # print(i['Instances'][0]['InstanceId'])

    table = prettytable.PrettyTable(['Name', 'InstanceId', 'Priv IP', 'Pub IP', 'Running'])
    table.align['Name'] = 'l'
    table.align['InstanceId'] = 'l'
    table.align['Priv IP'] = 'l'
    table.align['Pub IP'] = 'l'
    table.align['Running'] = 'l'
    table.padding_width = 1

    row = []
    for e in ec2_list:
        # pdb.set_trace()
        for inst in e['Instances']:
            instance_name = '   '  # Tags가 하나도 없을 경우를 대비

            '''
            'Tags'는 보통 'Instances' 내 아래와 같이 포함되어있다.
                ...
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": "k8s-node1"
                    }
                ],
                ...
            '''
            if 'Tags' in inst:  # Tag가 있다면
                for tag in inst['Tags']:
                    if tag['Key'] == 'Name':
                        # Tags에 있더라도 instance name에 해당하는 값이 없다면 '   '으로.
                        instance_name = tag['Value'] if tag['Value'] is not None else '   '
                        break

            row.append(instance_name)

            row.append(inst['InstanceId'])

            # If the instance's just terminated, it is still on the instance list
            # but no Private IP address.
            if 'PrivateIpAddress' in inst:
                row.append(inst['PrivateIpAddress'])
            else:
                row.append('N/A')

            if 'PublicIpAddress' in inst:
                row.append(inst['PublicIpAddress'])
            else:
                row.append('N/A')

            if inst['State']['Name'] == 'running':
                row.append('Y')
            else:
                row.append(' ')

            table.add_row(row)
            del row[:]

    print(table)


if __name__ == "__main__":
    run()
