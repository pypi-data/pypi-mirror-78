from aws_cdk import (
    aws_ec2 as ec2,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    core
)

from .utils import get_optional


class HalloumiVpcAlarms(object):

    LESS_THAN_THRESHOLD = (
        cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD
    )

    def __init__(
        self,
        scope,
        vpc,
        stack_name,
        alarmtopic,
        alarm_description
    ) -> None:

        # region Settings

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

        vpn_connection_state = None
        for node in vpc.node.find_all():
            if isinstance(node, ec2.VpnConnection):
                vpn_alarm_id = (
                    f'{stack_name}'
                    'VPNConnectionAlarm'
                    f'{node.node.id}'
                )
                vpn_connection_state = cloudwatch.Alarm(
                    scope,
                    vpn_alarm_id,
                    metric=node.metric_tunnel_state(),
                    evaluation_periods=evaluation_period,
                    threshold=1,
                    alarm_description=alarm_description,
                    comparison_operator=self.LESS_THAN_THRESHOLD,
                    period=period_vpn_state,
                    statistic='Maximum'
                )
                vpn_connection_state.add_alarm_action(
                    cloudwatch_actions.SnsAction(alarmtopic)
                )
