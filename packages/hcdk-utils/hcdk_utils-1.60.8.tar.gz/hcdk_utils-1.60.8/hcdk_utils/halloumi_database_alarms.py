from aws_cdk import (
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    core
)


class HalloumiDatabaseAlarms(object):

    def __init__(self, scope, stack_name, db_instances, alarm_topic):

        GREATER_THAN_OR_EQUAL_TO_THRESHOLD = (
            cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD
        )

        def __create_alarm(db_instance_id, stack_name, index):
            cpu_usage_high_alarm = cloudwatch.Alarm(
                scope,
                f'{stack_name}CPUUsageHighAlarm{index}',
                metric=cloudwatch.Metric(
                    metric_name='CPUUtilization',
                    namespace='AWS/RDS',
                    dimensions={
                        'DBInstanceIdentifier': db_instance_id
                    },
                    unit=cloudwatch.Unit.PERCENT
                ),
                evaluation_periods=1,
                threshold=80,
                alarm_description='Alarm for High CPU Utilization',
                comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                period=core.Duration.hours(6),
                statistic='Average',
            )
            cpu_usage_high_alarm.add_alarm_action(
                cloudwatch_actions.SnsAction(alarm_topic)
            )

            # Database Connections Alarm
            database_connections_alarm = cloudwatch.Alarm(
                scope,
                f'{stack_name}DatabaseConnectionsAlarm{index}',
                metric=cloudwatch.Metric(
                    metric_name='DatabaseConnections',
                    namespace='AWS/RDS',
                    dimensions={
                        'DBInstanceIdentifier': db_instance_id
                    },
                    unit=cloudwatch.Unit.COUNT
                ),
                evaluation_periods=1,
                threshold=50,
                alarm_description='Alarm for High Database Connections Count',
                comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                period=core.Duration.minutes(1),
                statistic='SampleCount',
                treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
            )
            database_connections_alarm.add_alarm_action(
                cloudwatch_actions.SnsAction(alarm_topic)
            )

            # Replication Lag Alarm
            replication_lag_alarm = cloudwatch.Alarm(
                scope,
                f'{stack_name}ReplicationLagAlarm{index}',
                metric=cloudwatch.Metric(
                    metric_name='AuroraReplicaLag',
                    namespace='AWS/RDS',
                    dimensions={
                        'DBInstanceIdentifier': db_instance_id
                    },
                    unit=cloudwatch.Unit.MILLISECONDS
                ),
                evaluation_periods=10,
                threshold=1_000,
                alarm_description='Alarm for High Replication Lag',
                comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
                period=core.Duration.minutes(1),
                statistic='Maximum',
                treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
            )
            replication_lag_alarm.add_alarm_action(
                cloudwatch_actions.SnsAction(alarm_topic)
            )

        self.alarms = [__create_alarm(d.ref, stack_name, index)
                       for index, d in enumerate(db_instances, start=1)]
