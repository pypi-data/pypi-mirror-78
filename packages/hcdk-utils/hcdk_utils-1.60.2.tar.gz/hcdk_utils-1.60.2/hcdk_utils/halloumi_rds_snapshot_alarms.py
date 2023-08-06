from aws_cdk import (
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cloudwatch_actions,
    core,
)


class HalloumiRdsSnapshotAlarms(object):

    def __init__(self, scope, stack_name, alarm_topic, retention_period):

        GREATER_THAN_OR_EQUAL_TO_THRESHOLD = (
            cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD
        )
        LESS_THAN_THRESHOLD = (
            cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD
        )

        _totalMetric = cloudwatch.Metric(
            metric_name='SnapshotCount',
            namespace=f'DCS/RDS/{stack_name}'
        )

        _hoursMetric = cloudwatch.Metric(
            metric_name='SnapshotAgeHours',
            namespace=f'DCS/RDS/{stack_name}'
        )

        # region Monitoring Alarms (total minimum)
        # :rds_not_enough_snapshots_alarms:
        _totalAlarm = cloudwatch.Alarm(
            scope,
            f'{stack_name}TotalCloudwatchAlarm',
            metric=_totalMetric,
            evaluation_periods=1,
            threshold=retention_period,
            actions_enabled=True,
            alarm_description='Alarm for too few RDS snapshots',
            comparison_operator=LESS_THAN_THRESHOLD,
            period=core.Duration.seconds(300),
            statistic='Minimum',
            treat_missing_data=cloudwatch.TreatMissingData.BREACHING
        )
        _totalAlarm.add_alarm_action(
            cloudwatch_actions.SnsAction(
                topic=alarm_topic
            )
        )
        # endregion
        # region Monitoring Alarms (Snapshot too old)
        # :rds_latest_snapshot_age_too_old_alarms:
        _tooOldAlarm = cloudwatch.Alarm(
            scope,
            f'{stack_name}TooOldCloudwatchAlarm',
            metric=_hoursMetric,
            evaluation_periods=1,
            threshold=47,
            actions_enabled=True,
            alarm_description=(
                f'Age of latest {stack_name} RDS '
                'snapshot too old, probably failing to copy snapshots'
            ),
            comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=core.Duration.hours(1),
            statistic='Minimum',
            treat_missing_data=cloudwatch.TreatMissingData.BREACHING
        )
        _tooOldAlarm.add_alarm_action(
            cloudwatch_actions.SnsAction(alarm_topic)
        )
        # endregion
        # region Monitoring Alarms (Expired Snapshot)
        # :rds_oldest_snapshot_age_too_old_alarms:
        _expiredAlarm = cloudwatch.Alarm(
            scope,
            f'{stack_name}ExpiredCloudwatchAlarm',
            metric=_hoursMetric,
            evaluation_periods=1,
            threshold=retention_period,
            actions_enabled=True,
            alarm_description=(
                'Alarm for oldest RDS snapshot age too old (needs cleanup)'
            ),
            comparison_operator=GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            period=core.Duration.hours(1),
            statistic='Maximum',
            treat_missing_data=cloudwatch.TreatMissingData.BREACHING
        )
        _expiredAlarm.add_alarm_action(
            cloudwatch_actions.SnsAction(alarm_topic)
        )
        # endregion
