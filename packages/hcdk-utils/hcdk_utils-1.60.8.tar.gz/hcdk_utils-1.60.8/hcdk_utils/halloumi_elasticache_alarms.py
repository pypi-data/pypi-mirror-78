from aws_cdk import (
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    core
)

from .utils import (
    get_optional
)


class HalloumiElasticacheAlarms(object):

    def __init__(
        self,
        scope,
        stack_name,
        cache_cluster_id,
        alarm_topic
    ):

        threshold_cpu_usage = int(get_optional(
            'ELASTICACHE_THRESHOLD_CPU_USAGE',
            80
        ))
        threshold_swap_usage = int(get_optional(
            'ELASTICACHE_THRESHOLD_SWAP_USAGE',
            50_000_000
        ))
        threshold_number_of_evictions = int(get_optional(
            'ELASTICACHE_THRESHOLD_HIGH_EVICTIONS',
            1_000_000_000
        ))
        threshold_number_of_connections = int(get_optional(
            'ELASTICACHE_THRESHOLD_HIGH_CONNECTIONS',
            10_000
        ))

        evaluation_period = int(get_optional(
            'ELASTICACHE_ALARM_EVALUATION_PERIOD',
            5
        ))

        period_cpu_usage = core.Duration.minutes(
            int(get_optional(
                'ELASTICACHE_PERIOD_CPU_USAGE',
                1
            ))
        )
        period_swap_usage = core.Duration.minutes(
            int(get_optional(
                'ELASTICACHE_PERIOD_SWAP_USAGE',
                1
            ))
        )
        period_number_of_evictions = core.Duration.minutes(
            int(get_optional(
                'ELASTICACHE_PERIOD_NUMBER_OF_EVICTIONS',
                1
            ))
        )
        period_number_of_connections = core.Duration.minutes(
            int(get_optional(
                'ELASTICACHE_PERIOD_NUMBER_OF_CONNECTIONS',
                1
            ))
        )

        # Elasticache High CPU Utilization
        elasticache_high_cpu_usage = cloudwatch.Alarm(
            scope, f'{stack_name}ElasticacheHighCpuUtilizationAlarm',
            metric=cloudwatch.Metric(
                metric_name='EngineCPUUtilization',
                namespace='AWS/ElastiCache',
                dimensions={
                    'CacheClusterId': cache_cluster_id
                },
                unit=cloudwatch.Unit.PERCENT
            ),
            evaluation_periods=evaluation_period,
            threshold=threshold_cpu_usage,
            alarm_description='Alarm for high CPU usage',
            comparison_operator=self.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=period_cpu_usage,
            statistic='Maximum'
        )
        elasticache_high_cpu_usage.add_alarm_action(
            cloudwatch_actions.SnsAction(alarm_topic)
        )

        # Elasticache High swap Usage
        elasticache_high_swap_usage = cloudwatch.Alarm(
            scope, f'{stack_name}ElasticacheHighSwapUsageAlarm',
            metric=cloudwatch.Metric(
                metric_name='SwapUsage',
                namespace='AWS/ElastiCache',
                dimensions={
                    'CacheClusterId': cache_cluster_id
                },
                unit=cloudwatch.Unit.BYTES
            ),
            evaluation_periods=evaluation_period,
            threshold=threshold_swap_usage,
            alarm_description='Alarm for high swap usage',
            comparison_operator=self.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=period_swap_usage,
            statistic='Average',
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        elasticache_high_swap_usage.add_alarm_action(
            cloudwatch_actions.SnsAction(alarm_topic)
        )

        # Elasticache High Number of Evictions
        elasticache_high_evictions = cloudwatch.Alarm(
            scope, f'{stack_name}ElasticacheHighEvictionsAlarm',
            metric=cloudwatch.Metric(
                metric_name='Evictions',
                namespace='AWS/ElastiCache',
                dimensions={
                    'CacheClusterId': cache_cluster_id
                },
                unit=cloudwatch.Unit.COUNT
            ),
            evaluation_periods=evaluation_period,
            threshold=threshold_number_of_evictions,
            alarm_description='Alarm for high number of evictions',
            comparison_operator=self.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=period_number_of_evictions,
            statistic='Average',
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        elasticache_high_evictions.add_alarm_action(
            cloudwatch_actions.SnsAction(alarm_topic)
        )

        # Elasticache High Number of Connections
        elasticache_high_connections = cloudwatch.Alarm(
            scope, f'{stack_name}ElasticacheHighConnectionsAlarm',
            metric=cloudwatch.Metric(
                metric_name='CurrConnections',
                namespace='AWS/ElastiCache',
                dimensions={
                    'CacheClusterId': cache_cluster_id
                },
                unit=cloudwatch.Unit.COUNT
            ),
            evaluation_periods=evaluation_period,
            threshold=threshold_number_of_connections,
            alarm_description='Alarm for high number of connections',
            comparison_operator=self.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=period_number_of_connections,
            statistic='Average',
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        elasticache_high_connections.add_alarm_action(
            cloudwatch_actions.SnsAction(alarm_topic)
        )
