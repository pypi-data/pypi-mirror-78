from aws_cdk import (
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    core
)

from .utils import (
    get_optional
)


class HalloumiDocumentDbAlarms(object):

    def __init__(self, scope, stack_name, db_instances, alarm_topic):
        GREATER_THAN_OR_EQUAL_TO_THRESHOLD = (
            cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD
        )

        # Configurable parameters for CloudWatch Alarms
        threshold_cpu_usage = int(get_optional(
            'DOCDB_THRESHOLD_CPU_USAGE',
            80
        ))
        threshold_number_of_connections = int(get_optional(
            'DOCDB_THRESHOLD_HIGH_CONNECTIONS',
            50
        ))
        threshold_replication_lag = int(get_optional(
            'DOCDB_THRESHOLD_REPLICATION_LAG',
            1000
        ))
        cpu_evaluation_period = int(get_optional(
            'DOCDB_CPU_EVALUATION_PERIOD',
            1
        ))
        connection_evaluation_period = int(get_optional(
            'DOCDB_CONNECTION_EVALUATION_PERIOD',
            1
        ))
        replication_evaluation_period = int(get_optional(
            'DOCDB_REPLICATION_EVALUATION_PERIOD',
            10
        ))
        period_cpu_usage = core.Duration.minutes(
            int(get_optional(
                'DOCDB_PERIOD_CPU_USAGE',
                1
            ))
        )
        period_number_of_connections = core.Duration.minutes(
            int(get_optional(
                'DOCDB_PERIOD_NUMBER_OF_CONNECTIONS',
                1
            ))
        )
        period_replication_lag = core.Duration.minutes(
            int(get_optional(
                'DOCDB_PERIOD_REPLICATION_LAG',
                1
            ))
        )

        def __create_alarm(db_instance_id, stack_name, index):

            # DB Alarms
            # CPU Usage High Alarm
            cpu_usage_high_alarm = cloudwatch.Alarm(
                self.__scope,
                f'{stack_name}DocdbCPUHighAlarm{index}',
                metric=cloudwatch.Metric(
                    metric_name='CPUUtilization',
                    namespace='AWS/DocDB',
                    dimensions={
                        'DBInstanceIdentifier': db_instance_id
                    },
                    unit=cloudwatch.Unit.PERCENT
                ),
                evaluation_periods=cpu_evaluation_period,
                threshold=threshold_cpu_usage,
                alarm_description=(
                    f'{self.short_env} - Alarm for High CPU Utilization'
                ),
                comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                period=period_cpu_usage,
                statistic='Average',
            )
            cpu_usage_high_alarm.add_alarm_action(
                cloudwatch_actions.SnsAction(alarm_topic)
            )

            # Database Connections Alarm
            database_connections_alarm = cloudwatch.Alarm(
                self.__scope,
                f'{stack_name}DocdbConnectionsAlarm{index}',
                metric=cloudwatch.Metric(
                    metric_name='DatabaseConnections',
                    namespace='AWS/DocDB',
                    dimensions={
                        'DBInstanceIdentifier': db_instance_id
                    },
                    unit=cloudwatch.Unit.COUNT
                ),
                evaluation_periods=connection_evaluation_period,
                threshold=threshold_number_of_connections,
                alarm_description=(
                    f'{self.short_env} - '
                    'Alarm for High Database Connections Count'
                ),
                comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                period=period_number_of_connections,
                statistic='SampleCount',
                treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
            )
            database_connections_alarm.add_alarm_action(
                cloudwatch_actions.SnsAction(alarm_topic)
            )

            # Replication Lag Alarm
            replication_lag_alarm = cloudwatch.Alarm(
                self.__scope,
                f'{stack_name}DocdbRepliLagAlarm{index}',
                metric=cloudwatch.Metric(
                    metric_name='DBInstanceReplicaLag',
                    namespace='AWS/DocDB',
                    dimensions={
                        'DBInstanceIdentifier': db_instance_id
                    },
                    unit=cloudwatch.Unit.MILLISECONDS
                ),
                evaluation_periods=replication_evaluation_period,
                threshold=threshold_replication_lag,
                alarm_description=(
                    f'{self.short_env} - Alarm for High Replication Lag'
                ),
                comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                period=period_replication_lag,
                statistic='Maximum',
                treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
            )
            replication_lag_alarm.add_alarm_action(
                cloudwatch_actions.SnsAction(alarm_topic)
            )
