from aws_cdk import (
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    core
)

from .utils import (
    get_optional,
    short_env
)


class HalloumiMqAlarms:
    def __init__(self,
                 scope,
                 broker_id,
                 stack_name,
                 alarmtopic):
        self.short_env = short_env()

        GREATER_THAN_OR_EQUAL_TO_THRESHOLD = (
            cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD
        )

        threshold_cpu_usage = int(get_optional(
            'AMQ_THRESHOLD_CPU_USAGE',
            80
        ))

        threshold_storage_usage = int(get_optional(
            'AMQ_THRESHOLD_STORAGE_USAGE',
            80
        ))

        evaluation_period = int(get_optional(
            'AMQ_EVALUATION_PERIOD',
            5
        ))

        # The environment variable should be set in minutes
        period_cpu_usage = core.Duration.minutes(
            int(get_optional(
                'AMQ_PERIOD_CPU_USAGE',
                1
            ))
        )
        period_storage_usage = core.Duration.minutes(
            int(get_optional(
                'AMQ_PERIOD_STORAGE_USAGE',
                1
            ))
        )

        # AmazonMQ High CPU Utilization
        amazonmq_high_cpu_usage = cloudwatch.Alarm(
            scope, f'{stack_name}AmazonMqHighCpuUtilizationAlarm',
            metric=cloudwatch.Metric(
                metric_name='CpuUtilization',
                namespace='AWS/AmazonMQ',
                dimensions={
                    'Broker': broker_id
                },
                unit=cloudwatch.Unit.PERCENT
            ),
            evaluation_periods=evaluation_period,
            threshold=threshold_cpu_usage,
            alarm_description=(
                f'{self.short_env} - Alarm for high CPU usage'
            ),
            comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=period_cpu_usage,
            statistic='Maximum'
        )
        amazonmq_high_cpu_usage.add_alarm_action(
            cloudwatch_actions.SnsAction(alarmtopic)
        )

        # AmazonMQ Storage Usage
        amazonmq_high_storage_usage = cloudwatch.Alarm(
            scope, f'{stack_name}AmazonMqHighStorageUsageAlarm',
            metric=cloudwatch.Metric(
                metric_name='StorePercentUsage',
                namespace='AWS/AmazonMQ',
                dimensions={
                    'Broker': broker_id
                },
                unit=cloudwatch.Unit.PERCENT
            ),
            evaluation_periods=evaluation_period,
            threshold=threshold_storage_usage,
            alarm_description=(
                f'{self.short_env} - Alarm for high storage usage'
            ),
            comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=period_storage_usage,
            statistic='Average',
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        amazonmq_high_storage_usage.add_alarm_action(
            cloudwatch_actions.SnsAction(alarmtopic)
        )
