from aws_cdk import (
    aws_autoscaling as asg,
    aws_iam as iam,
    aws_s3 as s3,
    core
)

from utils import (
    get_mandatory,
    ssm_parameter
)

from typing import List


class HalloumiOidc(object):

    __oidc = None

    def __init__(
        self,
        scope: core.Construct,
        config: dict,
        auto_scaling_group: asg.AutoScalingGroup,
        cluster_id: str = None,
        fileapi_bucket: s3.Bucket = None
    ) -> None:

        # region Settings
        self.auto_scaling_group = auto_scaling_group

        self.oidc_ca_thumbprint = get_mandatory(
            'OIDC_CA_THUMBPRINT'
        )

        region = get_mandatory(
            'AWS_REGION'
        )

        self.oidc_address = core.Fn.join(
            '/',
            [
                f'oidc.eks.{region}.amazonaws.com/id',
                cluster_id
            ]
        )

        self.__scope = scope
        self.stack_name = config["stack_name"]
        # endregion Settings

        # region ASG Role
        # Role to Manage AutoScalingGroup by K8S pods
        cluster_autoscale_policy = []
        cluster_autoscale_policy.append(
            iam.PolicyStatement(
                actions=[
                    "autoscaling:DescribeAutoScalingGroups",
                    "autoscaling:DescribeAutoScalingInstances",
                    "autoscaling:DescribeLaunchConfigurations",
                    "autoscaling:DescribeTags",
                    "ec2:DescribeLaunchTemplateVersions"
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )
        cluster_autoscale_policy.append(
            iam.PolicyStatement(
                actions=[
                    "autoscaling:SetDesiredCapacity",
                    "autoscaling:TerminateInstanceInAutoScalingGroup"
                ],
                effect=iam.Effect.ALLOW,
                resources=[self.auto_scaling_group.auto_scaling_group_arn]
            )
        )

        self.oidc_role(
            scope=scope,
            role_id=f'{config["stack_name"]}AutoscaleIamRole',
            statements=cluster_autoscale_policy,
            serviceaccount='cluster-autoscaler'
        )
        # endregion ASG Role

        # region ELB Role
        # IAM Role to access the Elastic Loadbalancing from K8s
        elb_iam_role_id = (
            f'{config["stack_name"]}ELBIamRole'
        )
        # Attach the policies to the IAM Role
        elb_policy = []
        elb_policy.append(
            iam.PolicyStatement(
                actions=[
                    'acm:DescribeCertificate',
                    'acm:ListCertificates',
                    'acm:GetCertificate'
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        elb_policy.append(
            iam.PolicyStatement(
                actions=[
                    'ec2:AuthorizeSecurityGroupIngress',
                    'ec2:CreateSecurityGroup',
                    'ec2:CreateTags',
                    'ec2:DeleteTags',
                    'ec2:DeleteSecurityGroup',
                    'ec2:DescribeAccountAttributes',
                    'ec2:DescribeAddresses',
                    'ec2:DescribeInstances',
                    'ec2:DescribeInstanceStatus',
                    'ec2:DescribeInternetGateways',
                    'ec2:DescribeNetworkInterfaces',
                    'ec2:DescribeSecurityGroups',
                    'ec2:DescribeSubnets',
                    'ec2:DescribeTags',
                    'ec2:DescribeVpcs',
                    'ec2:ModifyInstanceAttribute',
                    'ec2:ModifyNetworkInterfaceAttribute',
                    'ec2:RevokeSecurityGroupIngress'
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        elb_policy.append(
            iam.PolicyStatement(
                actions=[
                    'elasticloadbalancing:AddListenerCertificates',
                    'elasticloadbalancing:AddTags',
                    'elasticloadbalancing:CreateListener',
                    'elasticloadbalancing:CreateLoadBalancer',
                    'elasticloadbalancing:CreateRule',
                    'elasticloadbalancing:CreateTargetGroup',
                    'elasticloadbalancing:DeleteListener',
                    'elasticloadbalancing:DeleteLoadBalancer',
                    'elasticloadbalancing:DeleteRule',
                    'elasticloadbalancing:DeleteTargetGroup',
                    'elasticloadbalancing:DeregisterTargets',
                    'elasticloadbalancing:DescribeListenerCertificates',
                    'elasticloadbalancing:DescribeListeners',
                    'elasticloadbalancing:DescribeLoadBalancers',
                    'elasticloadbalancing:DescribeLoadBalancerAttributes',
                    'elasticloadbalancing:DescribeRules',
                    'elasticloadbalancing:DescribeSSLPolicies',
                    'elasticloadbalancing:DescribeTags',
                    'elasticloadbalancing:DescribeTargetGroups',
                    'elasticloadbalancing:DescribeTargetGroupAttributes',
                    'elasticloadbalancing:DescribeTargetHealth',
                    'elasticloadbalancing:ModifyListener',
                    'elasticloadbalancing:ModifyLoadBalancerAttributes',
                    'elasticloadbalancing:ModifyRule',
                    'elasticloadbalancing:ModifyTargetGroup',
                    'elasticloadbalancing:ModifyTargetGroupAttributes',
                    'elasticloadbalancing:RegisterTargets',
                    'elasticloadbalancing:RemoveListenerCertificates',
                    'elasticloadbalancing:RemoveTags',
                    'elasticloadbalancing:SetIpAddressType',
                    'elasticloadbalancing:SetSecurityGroups',
                    'elasticloadbalancing:SetSubnets',
                    'elasticloadbalancing:SetWebACL'
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        elb_policy.append(
            iam.PolicyStatement(
                actions=[
                    'iam:CreateServiceLinkedRole',
                    'iam:GetServerCertificate',
                    'iam:ListServerCertificates'
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        elb_policy.append(
            iam.PolicyStatement(
                actions=[
                    'waf-regional:GetWebACLForResource',
                    'waf-regional:GetWebACL',
                    'waf-regional:AssociateWebACL',
                    'waf-regional:DisassociateWebACL'
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        elb_policy.append(
            iam.PolicyStatement(
                actions=[
                    'tag:GetResources',
                    'tag:TagResources'
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        elb_policy.append(
            iam.PolicyStatement(
                actions=[
                    'waf:GetWebACL'
                ],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )
        self.oidc_role(
            scope=scope,
            role_id=elb_iam_role_id,
            statements=elb_policy,
            serviceaccount='alb-ingress-controller'
        )
        # endregion ELB Role

        # region Route53 Role
        # IAM Role to access Route53 from K8S Pods
        route53_policy = []
        route53_policy.append(
            iam.PolicyStatement(
                actions=[
                    "route53:ChangeResourceRecordSets"
                ],
                effect=iam.Effect.ALLOW,
                resources=[
                    'arn:aws:route53:::hostedzone/*'
                ]
            )
        )
        route53_policy.append(
            iam.PolicyStatement(
                actions=[
                    "route53:ListHostedZones",
                    "route53:ListResourceRecordSets"
                ],
                effect=iam.Effect.ALLOW,
                resources=["*"]
            )
        )
        self.oidc_role(
            scope=scope,
            role_id=f'{config["stack_name"]}Route53IamRole',
            statements=route53_policy,
            serviceaccount='external-dns',
            namespace='default'
        )
        # endregion Route53 Role

        # region FileApi Bucket role
        fileapi_oidc_role = self.oidc_role(
            scope=scope,
            role_id=f'{config["stack_name"]}FileApiIamRole',
            statements=[],
            serviceaccount='file-api',
            namespace='default'
        )

        fileapi_bucket.grant_read_write(fileapi_oidc_role)
        # endregion

    def oidc_role(
        self,
        scope: core.Construct,
        role_id: str,
        statements: List[iam.PolicyStatement],
        serviceaccount: str,
        namespace: str = 'kube-system',
        oidc_principal: iam.OpenIdConnectProvider = None
    ) -> iam.Role:

        if not oidc_principal:
            oidc_principal = self.oidc_provider
        condition = core.CfnJson(
            scope,
            f'{role_id}Condition',
            value={
                f"{self.oidc_address}:sub": (
                    f"system:serviceaccount:{namespace}:{serviceaccount}"
                )
            }
        )
        oidc_principal_base = iam.OpenIdConnectPrincipal(
            open_id_connect_provider=oidc_principal
        )
        oidc_principal = oidc_principal_base.with_conditions(
            conditions={
                "StringEquals": condition
            }
        )
        role = iam.Role(
            scope, role_id,
            assumed_by=oidc_principal
        )
        for policy in statements:
            role.add_to_policy(statement=policy)

        ssm_parameter.save(
            scope=scope,
            section='k8s',
            key='SA_%s' % serviceaccount.upper(),
            value=role.role_arn
        )

        return role

    @property
    def oidc_provider(self) -> iam.OpenIdConnectProvider:
        if self.__oidc is None:
            oidc_principal_id = (
                f'{self.stack_name}OIDCPrincipal'
            )
            self.__oidc = iam.OpenIdConnectProvider(
                self.__scope,
                oidc_principal_id,
                client_ids=['sts.amazonaws.com'],
                thumbprints=[self.oidc_ca_thumbprint],
                url=f'https://{self.oidc_address}'
            )
        return self.__oidc
