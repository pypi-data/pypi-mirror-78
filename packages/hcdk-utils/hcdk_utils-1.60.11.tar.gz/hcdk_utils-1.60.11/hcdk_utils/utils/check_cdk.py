import subprocess
import os


def check_cdk():
    CDK_VERSION = os.getenv('CDK_VERSION')
    # Check whether the expected version of the AWS CDK CLI is used
    reported_cdk_cli = subprocess.check_output(['cdk', '--version'])
    if not reported_cdk_cli.startswith(CDK_VERSION.encode('utf-8')):
        print(f'Reported AWS CDK CLI version is {reported_cdk_cli}')
        print(f'Expected AWS CDK CLI version is {CDK_VERSION}')
        raise ValueError('Unexpected version for the AWS CDK CLI')

    # Check whether the expected version of the modules is used
    # We assume that we use the same module version for all
    # aws-cdk components
    expected_cdk_module = f'aws-cdk.core=={CDK_VERSION}\n'
    rep = subprocess.check_output(['pip freeze | grep aws-cdk.core'],
                                  shell=True)
    if expected_cdk_module.encode('utf-8') != rep:
        print(f'Reported AWS CDK module version is {rep}')
        print(f'Expected AWS CDK module version is {expected_cdk_module}')
        raise ValueError('Unexpected version for the AWS CDK module')
