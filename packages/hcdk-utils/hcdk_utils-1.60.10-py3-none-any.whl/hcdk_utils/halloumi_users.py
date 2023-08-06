from aws_cdk import (
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    core
)


class HalloumiUsers(object):
    def __init__(
        self,
        scope: core.Construct,
        config: dict,
        **kwargs,
    ) -> None:

        self.__users = {}
        for user in config.get('users', []):
            if self.__users.get(user):
                continue
            new_user = iam.User(
                scope,
                f'{config["stack_name"]}{user}-User',
                user_name=user
            )
            access_keys = iam.CfnAccessKey(
                scope,
                f'{config["stack_name"]}{user}-AccessKeys',
                user_name=new_user.user_name,
                status='Active'
            )
            secret_key = core.Fn.get_att(
                access_keys.logical_id,
                'SecretAccessKey'
            )
            credentials = secretsmanager.CfnSecret(
                scope,
                f'{config["stack_name"]}{user}-SecretAccessKeys',
                description=f'{user} secret and access keys',
                secret_string='{"access_key": "%s", "secret_key": "%s"}' % (
                    access_keys.ref,
                    secret_key.to_string()
                )
            )
            credentials.add_depends_on(access_keys)
            self.__users[user] = new_user

    @property
    def users(self) -> [iam.User]:
        return self.__users

    def user(self, name: str) -> iam.User:
        if self.__users.get(name):
            return self.__users.get(name)
        raise Exception("User %s not defined" % name)
