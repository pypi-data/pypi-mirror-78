"""
[![NPM version](https://badge.fury.io/js/cdk-gitlab-runner.svg)](https://badge.fury.io/js/cdk-gitlab-runner)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab-runner.svg)](https://badge.fury.io/py/cdk-gitlab-runner)
![Release](https://github.com/guan840912/cdk-gitlab-runner/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-gitlab-runner?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-gitlab-runner?label=pypi&color=blue)

![](https://img.shields.io/badge/iam_role_self-enable-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/vpc_self-enable-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/gitlab_url-customize-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/spotfleet-runner-green=?style=plastic&logo=appveyor)

# Welcome to `cdk-gitlab-runner`

This repository template helps you create gitlab runner on your aws account via AWS CDK one line.

## Note

### Default will help you generate below services:

* VPC

  * Public Subnet (2)
* EC2 (1 T3.micro)

## Before start you need gitlab runner token in your `gitlab project` or `gitlab group`

### In Group

Group > Settings > CI/CD
![group](image/group_runner_page.png)

### In Group

Project > Settings > CI/CD > Runners
![project](image/project_runner_page.png)

## Usage

Replace your gitlab runner token in `$GITLABTOKEN`

### Instance Type

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner

# If want change instance type to t3.large .
GitlabContainerRunner(self, "runner-instance", gitlabtoken="$GITLABTOKEN", ec2type="t3.large")
# OR
# Just create a gitlab runner , by default instance type is t3.micro .
from cdk_gitlab_runner import GitlabContainerRunner

GitlabContainerRunner(self, "runner-instance", gitlabtoken="$GITLABTOKEN")
```

### Gitlab Server Customize Url .

If you want change what you want tag name .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want change  what  your self Gitlab Server Url .
from cdk_gitlab_runner import GitlabContainerRunner

GitlabContainerRunner(self, "runner-instance-change-tag",
    gitlabtoken="$GITLABTOKEN",
    gitlaburl="https://gitlab.my.com/"
)
```

### Tags

If you want change what you want tag name .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want change  what  you want tag name .
from cdk_gitlab_runner import GitlabContainerRunner

GitlabContainerRunner(self, "runner-instance-change-tag",
    gitlabtoken="$GITLABTOKEN",
    tag1="aa",
    tag2="bb",
    tag3="cc"
)
```

### IAM Policy

If you want add runner other IAM Policy like s3-readonly-access.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want add runner other IAM Policy like s3-readonly-access.
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_iam import ManagedPolicy

runner = GitlabContainerRunner(self, "runner-instance-add-policy",
    gitlabtoken="$GITLABTOKEN",
    tag1="aa",
    tag2="bb",
    tag3="cc"
)
runner.runner_role.add_managed_policy(
    ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))
```

### Security Group

If you want add runner other SG Ingress .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# If you want add runner other SG Ingress .
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import Port, Peer

runner = GitlabContainerRunner(self, "runner-add-SG-ingress",
    gitlabtoken="GITLABTOKEN",
    tag1="aa",
    tag2="bb",
    tag3="cc"
)

# you can add ingress in your runner SG .
runner.default_runner_sG.connections.allow_from(
    Peer.ipv4("0.0.0.0/0"),
    Port.tcp(80))
```

### Use self VPC

> 2020/06/27 , you can use your self exist VPC or new VPC , but please check your `vpc public Subnet` Auto-assign public IPv4 address must be Yes ,or `vpc private Subnet` route table associated `nat gateway` .

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import Port, Peer, Vpc, SubnetType
from aws_cdk.aws_iam import ManagedPolicy

newvpc = Vpc(stack, "VPC",
    cidr="10.1.0.0/16",
    max_azs=2,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="RunnerVPC",
        subnet_type=SubnetType.PUBLIC
    )
    ],
    nat_gateways=0
)

runner = GitlabContainerRunner(self, "testing",
    gitlabtoken="$GITLABTOKEN",
    ec2type="t3.small",
    selfvpc=newvpc
)
```

### Use your self exist role

> 2020/06/27 , you can use your self exist role assign to runner

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner
from aws_cdk.aws_ec2 import Port, Peer
from aws_cdk.aws_iam import ManagedPolicy, Role, ServicePrincipal

role = Role(self, "runner-role",
    assumed_by=ServicePrincipal("ec2.amazonaws.com"),
    description="For Gitlab EC2 Runner Test Role",
    role_name="TestRole"
)

runner = GitlabContainerRunner(stack, "testing",
    gitlabtoken="$GITLAB_TOKEN",
    ec2iamrole=role
)
runner.runner_role.add_managed_policy(
    ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"))
```

### Custom Gitlab Runner EBS szie

> 2020/08/22 , you can change you want ebs size.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner

GitlabContainerRunner(stack, "testing",
    gitlabtoken="$GITLAB_TOKEN",
    ebs_size=50
)
```

### Support Spotfleet Gitlab Runner

> 2020/08/27 , you can use spotfleet instance be your gitlab runner,
> after create spotfleet instance will auto output instance id .thank [@pahud](https://github.com/pahud/cdk-spot-one) again ~~~

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner, BlockDuration

runner = GitlabContainerRunner(stack, "testing",
    gitlabtoken="GITLAB_TOKEN",
    ec2type="t3.large",
    block_duration=BlockDuration.ONE_HOUR,
    spot_fleet=True
)
# configure the expiration after 1 hours
runner.expire_after(Duration.hours(1))
```

# Note

![](https://img.shields.io/badge/version-1.47.1-green=?style=plastic&logo=appveyor) vs ![](https://img.shields.io/badge/version-1.49.1-green=?style=plastic&logo=appveyor)

> About change instance type

This is before ![](https://img.shields.io/badge/version-1.47.1-green=?style) ( included ![](https://img.shields.io/badge/version-1.47.1-green=?style) )

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ec2 import InstanceType, InstanceClass, InstanceSize
from cdk_gitlab_runner import GitlabContainerRunner

# If want change instance type to t3.large .
GitlabContainerRunner(self, "runner-instance",
    gitlabtoken="$GITLABTOKEN",
    ec2type=InstanceType.of(InstanceClass.T3, InstanceSize.LARGE)
)
```

This is ![](https://img.shields.io/badge/version-1.49.1-green=?style)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab_runner import GitlabContainerRunner

# If want change instance type to t3.large .
GitlabContainerRunner(self, "runner-instance",
    gitlabtoken="$GITLABTOKEN",
    ec2type="t3.large"
)
```

## Wait about 6 mins , If success you will see your runner in that page .

![runner](image/group_runner2.png)

#### you can use tag `gitlab` , `runner` , `awscdk` ,

## Example *`gitlab-ci.yaml`*

[gitlab docs see more ...](https://docs.gitlab.com/ee/ci/yaml/README.html)

```yaml
dockerjob:
  image: docker:18.09-dind
  variables:
  tags:
    - runner
    - awscdk
    - gitlab
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker info
  script:
    - docker info;
    - echo 'test 123';
    - echo 'hello world 1228'
```

### If your want to debug you can go to aws console

# `In your runner region !!!`

## AWS Systems Manager > Session Manager > Start a session

![system manager](image/session.png)

#### click your `runner` and click `start session`

#### in the brower console in put `bash`

```bash
# become to root
sudo -i

# list runner container .
root# docker ps -a

# modify gitlab-runner/config.toml

root# cd /home/ec2-user/.gitlab-runner/ && ls
config.toml

```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.core


@jsii.enum(jsii_type="cdk-gitlab-runner.BlockDuration")
class BlockDuration(enum.Enum):
    ONE_HOUR = "ONE_HOUR"
    TWO_HOURS = "TWO_HOURS"
    THREE_HOURS = "THREE_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    FIVE_HOURS = "FIVE_HOURS"
    SIX_HOURS = "SIX_HOURS"
    SEVEN_HOURS = "SEVEN_HOURS"
    EIGHT_HOURS = "EIGHT_HOURS"
    NINE_HOURS = "NINE_HOURS"
    TEN_HOURS = "TEN_HOURS"
    ELEVEN_HOURS = "ELEVEN_HOURS"
    TWELVE_HOURS = "TWELVE_HOURS"
    THIRTEEN_HOURS = "THIRTEEN_HOURS"
    FOURTEEN_HOURS = "FOURTEEN_HOURS"
    FIFTEEN_HOURS = "FIFTEEN_HOURS"
    SIXTEEN_HOURS = "SIXTEEN_HOURS"
    SEVENTEEN_HOURS = "SEVENTEEN_HOURS"
    EIGHTTEEN_HOURS = "EIGHTTEEN_HOURS"
    NINETEEN_HOURS = "NINETEEN_HOURS"
    TWENTY_HOURS = "TWENTY_HOURS"


class GitlabContainerRunner(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab-runner.GitlabContainerRunner",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        gitlabtoken: builtins.str,
        block_duration: typing.Optional["BlockDuration"] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        ec2iamrole: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        ec2type: typing.Optional[builtins.str] = None,
        gitlaburl: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"] = None,
        key_name: typing.Optional[builtins.str] = None,
        selfvpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        spot_fleet: typing.Optional[builtins.bool] = None,
        tag1: typing.Optional[builtins.str] = None,
        tag2: typing.Optional[builtins.str] = None,
        tag3: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
        vpc_subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param gitlabtoken: Gitlab token for the Register Runner . Default: - You must to give the token !!!
        :param block_duration: Reservce the Spot Runner instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR , !!! only support spotfleet runner !!! .
        :param ebs_size: Gitlab Runner instance EBS size . Default: - ebsSize=60
        :param ec2iamrole: IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param ec2type: Runner default EC2 instance type. Default: - t3.micro
        :param gitlaburl: Gitlab Runner register url . Default: - gitlaburl='https://gitlab.com/'
        :param instance_interruption_behavior: The behavior when a Spot Runner Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE , !!! only support spotfleet runner !!! .
        :param key_name: SSH key name. Default: - no ssh key will be assigned , !!! only support spotfleet runner !!! .
        :param selfvpc: VPC for the Gitlab Runner . Default: - new VPC will be created , 1 Vpc , 2 Public Subnet .
        :param spot_fleet: Gitlab Runner instance Use Spot Fleet or not ?!. Default: - spotFleet=false
        :param tag1: Gitlab Runner register tag1 . Default: - tag1: gitlab .
        :param tag2: Gitlab Runner register tag2 . Default: - tag2: awscdk .
        :param tag3: Gitlab Runner register tag3 . Default: - tag3: runner .
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration , !!! only support spotfleet runner !!! .
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        """
        props = GitlabContainerRunnerProps(
            gitlabtoken=gitlabtoken,
            block_duration=block_duration,
            ebs_size=ebs_size,
            ec2iamrole=ec2iamrole,
            ec2type=ec2type,
            gitlaburl=gitlaburl,
            instance_interruption_behavior=instance_interruption_behavior,
            key_name=key_name,
            selfvpc=selfvpc,
            spot_fleet=spot_fleet,
            tag1=tag1,
            tag2=tag2,
            tag3=tag3,
            valid_until=valid_until,
            vpc_subnet=vpc_subnet,
        )

        jsii.create(GitlabContainerRunner, self, [scope, id, props])

    @jsii.member(jsii_name="expireAfter")
    def expire_after(self, duration: aws_cdk.core.Duration) -> None:
        """
        :param duration: -

        default
        :default: - !!! only support spotfleet runner !!! .
        """
        return jsii.invoke(self, "expireAfter", [duration])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultRunnerSG")
    def default_runner_sg(self) -> aws_cdk.aws_ec2.ISecurityGroup:
        return jsii.get(self, "defaultRunnerSG")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="runnerEc2")
    def runner_ec2(self) -> aws_cdk.aws_ec2.IInstance:
        """This represents a Runner EC2 instance , !!! only support On-demand runner instance !!! ."""
        return jsii.get(self, "runnerEc2")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="runnerRole")
    def runner_role(self) -> aws_cdk.aws_iam.IRole:
        """The IAM role assumed by the Runner instance ."""
        return jsii.get(self, "runnerRole")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="spotFleetInstanceId")
    def spot_fleet_instance_id(self) -> builtins.str:
        """the first instance id in this fleet , !!! only support spotfleet runner !!! ."""
        return jsii.get(self, "spotFleetInstanceId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="spotFleetRequestId")
    def spot_fleet_request_id(self) -> builtins.str:
        """SpotFleetRequestId for this spot fleet , !!! only support spotfleet runner !!! ."""
        return jsii.get(self, "spotFleetRequestId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")


@jsii.data_type(
    jsii_type="cdk-gitlab-runner.GitlabContainerRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "gitlabtoken": "gitlabtoken",
        "block_duration": "blockDuration",
        "ebs_size": "ebsSize",
        "ec2iamrole": "ec2iamrole",
        "ec2type": "ec2type",
        "gitlaburl": "gitlaburl",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "key_name": "keyName",
        "selfvpc": "selfvpc",
        "spot_fleet": "spotFleet",
        "tag1": "tag1",
        "tag2": "tag2",
        "tag3": "tag3",
        "valid_until": "validUntil",
        "vpc_subnet": "vpcSubnet",
    },
)
class GitlabContainerRunnerProps:
    def __init__(
        self,
        *,
        gitlabtoken: builtins.str,
        block_duration: typing.Optional["BlockDuration"] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        ec2iamrole: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        ec2type: typing.Optional[builtins.str] = None,
        gitlaburl: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"] = None,
        key_name: typing.Optional[builtins.str] = None,
        selfvpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        spot_fleet: typing.Optional[builtins.bool] = None,
        tag1: typing.Optional[builtins.str] = None,
        tag2: typing.Optional[builtins.str] = None,
        tag3: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
        vpc_subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param gitlabtoken: Gitlab token for the Register Runner . Default: - You must to give the token !!!
        :param block_duration: Reservce the Spot Runner instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR , !!! only support spotfleet runner !!! .
        :param ebs_size: Gitlab Runner instance EBS size . Default: - ebsSize=60
        :param ec2iamrole: IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param ec2type: Runner default EC2 instance type. Default: - t3.micro
        :param gitlaburl: Gitlab Runner register url . Default: - gitlaburl='https://gitlab.com/'
        :param instance_interruption_behavior: The behavior when a Spot Runner Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE , !!! only support spotfleet runner !!! .
        :param key_name: SSH key name. Default: - no ssh key will be assigned , !!! only support spotfleet runner !!! .
        :param selfvpc: VPC for the Gitlab Runner . Default: - new VPC will be created , 1 Vpc , 2 Public Subnet .
        :param spot_fleet: Gitlab Runner instance Use Spot Fleet or not ?!. Default: - spotFleet=false
        :param tag1: Gitlab Runner register tag1 . Default: - tag1: gitlab .
        :param tag2: Gitlab Runner register tag2 . Default: - tag2: awscdk .
        :param tag3: Gitlab Runner register tag3 . Default: - tag3: runner .
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration , !!! only support spotfleet runner !!! .
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        """
        if isinstance(vpc_subnet, dict):
            vpc_subnet = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnet)
        self._values: typing.Dict[str, typing.Any] = {
            "gitlabtoken": gitlabtoken,
        }
        if block_duration is not None:
            self._values["block_duration"] = block_duration
        if ebs_size is not None:
            self._values["ebs_size"] = ebs_size
        if ec2iamrole is not None:
            self._values["ec2iamrole"] = ec2iamrole
        if ec2type is not None:
            self._values["ec2type"] = ec2type
        if gitlaburl is not None:
            self._values["gitlaburl"] = gitlaburl
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if key_name is not None:
            self._values["key_name"] = key_name
        if selfvpc is not None:
            self._values["selfvpc"] = selfvpc
        if spot_fleet is not None:
            self._values["spot_fleet"] = spot_fleet
        if tag1 is not None:
            self._values["tag1"] = tag1
        if tag2 is not None:
            self._values["tag2"] = tag2
        if tag3 is not None:
            self._values["tag3"] = tag3
        if valid_until is not None:
            self._values["valid_until"] = valid_until
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet

    @builtins.property
    def gitlabtoken(self) -> builtins.str:
        """Gitlab token for the Register Runner .

        default
        :default: - You must to give the token !!!

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN")
        """
        result = self._values.get("gitlabtoken")
        assert result is not None, "Required property 'gitlabtoken' is missing"
        return result

    @builtins.property
    def block_duration(self) -> typing.Optional["BlockDuration"]:
        """Reservce the Spot Runner instance as spot block with defined duration.

        default
        :default: - BlockDuration.ONE_HOUR , !!! only support spotfleet runner !!! .
        """
        result = self._values.get("block_duration")
        return result

    @builtins.property
    def ebs_size(self) -> typing.Optional[jsii.Number]:
        """Gitlab Runner instance EBS size .

        default
        :default: - ebsSize=60

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            runner = GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", ebs_size=100)
        """
        result = self._values.get("ebs_size")
        return result

    @builtins.property
    def ec2iamrole(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """IAM role for the Gitlab Runner Instance .

        default
        :default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            role = Role(stack, "runner-role",
                assumed_by=ServicePrincipal("ec2.amazonaws.com"),
                description="For Gitlab EC2 Runner Test Role",
                role_name="Myself-Runner-Role"
            )
            
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", ec2iamrole=role)
        """
        result = self._values.get("ec2iamrole")
        return result

    @builtins.property
    def ec2type(self) -> typing.Optional[builtins.str]:
        """Runner default EC2 instance type.

        default
        :default: - t3.micro

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", ec2type="t3.small")
        """
        result = self._values.get("ec2type")
        return result

    @builtins.property
    def gitlaburl(self) -> typing.Optional[builtins.str]:
        """Gitlab Runner register url .

        default
        :default: - gitlaburl='https://gitlab.com/'

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            runner = GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", gitlaburl="https://gitlab.com/")
        """
        result = self._values.get("gitlaburl")
        return result

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional["InstanceInterruptionBehavior"]:
        """The behavior when a Spot Runner Instance is interrupted.

        default
        :default: - InstanceInterruptionBehavior.TERMINATE , !!! only support spotfleet runner !!! .
        """
        result = self._values.get("instance_interruption_behavior")
        return result

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        """SSH key name.

        default
        :default: - no ssh key will be assigned , !!! only support spotfleet runner !!! .
        """
        result = self._values.get("key_name")
        return result

    @builtins.property
    def selfvpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC for the Gitlab Runner .

        default
        :default: - new VPC will be created , 1 Vpc , 2 Public Subnet .

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            newvpc = Vpc(stack, "NEWVPC",
                cidr="10.1.0.0/16",
                max_azs=2,
                subnet_configuration=[{
                    "cidr_mask": 26,
                    "name": "RunnerVPC",
                    "subnet_type": SubnetType.PUBLIC
                }],
                nat_gateways=0
            )
            
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", selfvpc=newvpc)
        """
        result = self._values.get("selfvpc")
        return result

    @builtins.property
    def spot_fleet(self) -> typing.Optional[builtins.bool]:
        """Gitlab Runner instance Use Spot Fleet or not ?!.

        default
        :default: - spotFleet=false

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            runner = GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", spot_fleet=True)
        """
        result = self._values.get("spot_fleet")
        return result

    @builtins.property
    def tag1(self) -> typing.Optional[builtins.str]:
        """Gitlab Runner register tag1  .

        default
        :default: - tag1: gitlab .

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", tag1="aa")
        """
        result = self._values.get("tag1")
        return result

    @builtins.property
    def tag2(self) -> typing.Optional[builtins.str]:
        """Gitlab Runner register tag2  .

        default
        :default: - tag2: awscdk .

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", tag2="bb")
        """
        result = self._values.get("tag2")
        return result

    @builtins.property
    def tag3(self) -> typing.Optional[builtins.str]:
        """Gitlab Runner register tag3  .

        default
        :default: - tag3: runner .

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitlabContainerRunner(stack, "runner", gitlabtoken="GITLAB_TOKEN", tag3="cc")
        """
        result = self._values.get("tag3")
        return result

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        """the time when the spot fleet allocation expires.

        default
        :default: - no expiration , !!! only support spotfleet runner !!! .
        """
        result = self._values.get("valid_until")
        return result

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC subnet for the spot fleet.

        default
        :default: - public subnet

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            vpc = Vpc(stack, "nat",
                nat_gateways=1,
                max_azs=2
            )
            runner = GitlabContainerRunner(stack, "testing",
                gitlabtoken="GITLAB_TOKEN",
                ec2type="t3.large",
                ec2iamrole=role,
                ebs_size=100,
                selfvpc=vpc,
                vpc_subnet={
                    "subnet_type": SubnetType.PUBLIC
                }
            )
        """
        result = self._values.get("vpc_subnet")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitlabContainerRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-gitlab-runner.InstanceInterruptionBehavior")
class InstanceInterruptionBehavior(enum.Enum):
    HIBERNATE = "HIBERNATE"
    STOP = "STOP"
    TERMINATE = "TERMINATE"


__all__ = [
    "BlockDuration",
    "GitlabContainerRunner",
    "GitlabContainerRunnerProps",
    "InstanceInterruptionBehavior",
]

publication.publish()
