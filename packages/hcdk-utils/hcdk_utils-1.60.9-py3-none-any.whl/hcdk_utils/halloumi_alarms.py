from aws_cdk import (
    aws_ec2 as ec2,
    aws_sns as sns,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    core
)
from utils import get_optional, private_stack_name
from typing import Dict


class HalloumiVpcAlarms(object):

    LESS_THAN_THRESHOLD = (
        cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD
    )

    def __init__(
        self,
        scope: core.Construct,
        vpc: ec2.IVpc,
        topics: Dict[str, sns.Topic]
    ) -> None:

        # region Settings
        self.stack_name = private_stack_name()

        co_gateway_ip = get_optional('CUSTOMER_GATEWAY_IP')

        # Configurable parameters for CloudWatch Alarms
        evaluation_period = int(get_optional(
            'VPN_CONNECTION_ALARM_EVALUATION_PERIOD',
            5
        ))

        # The environment variable should be set in minutes
        period_vpn_state = core.Duration.minutes(
            int(get_optional(
                'VPN_CONNECTION_PERIOD',
                1
            ))
        )
        # endregion Settings

        if co_gateway_ip:
            vpn_alarm = None
            vpn_connection_state = None
            for node in vpc.node.find_all():
                if isinstance(node, ec2.VpnConnection):
                    vpn_alarm = 'ProData'
                    vpn_alarm_id = (
                        f'{self.stack_name}'
                        'VPNConnectionAlarm'
                        f'{vpn_alarm}'
                    )
                    vpn_connection_state = cloudwatch.Alarm(
                        scope,
                        vpn_alarm_id,
                        metric=node.metric_tunnel_state(),
                        evaluation_periods=evaluation_period,
                        threshold=1,
                        alarm_description=(
                            f'Alarm for {vpn_alarm} VPN Connection State'
                        ),
                        comparison_operator=self.LESS_THAN_THRESHOLD,
                        period=period_vpn_state,
                        statistic='Maximum'
                    )
                    vpn_connection_state.add_alarm_action(
                        cloudwatch_actions.SnsAction(topics['l1'])
                    )