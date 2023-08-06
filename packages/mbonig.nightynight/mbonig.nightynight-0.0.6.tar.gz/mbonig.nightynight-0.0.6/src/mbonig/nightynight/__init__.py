"""
# NightyNight!

Do you have a EC2 instance that you only need during certain hours of the day? Do you want to reduce it's cost? How about just stopping it every night?

That's the NightyNight construct. It's very simple. Give it an `instanceId` and it will create a Lambda and a CloudWatch Event Rule to fire the lambda at a specific time of day. If the instance is running, it's stopped.

# This is a pre-release!

This is a quick first-draft. All the options that will likely need to be added to accomodate a large
number of use-cases are still needed. If you'd like to make requests or help update this construct, please
open an [Issue](https://github.com/mbonig/nightynight/issues) or a [PR](https://github.com/mbonig/cicd-spa-website/pulls).

# What is creates

![arch.png](./arch.png)

* A Rule that will, on a given schedule, fire a lambda.
* A Lambda with permissions to describe ec2 instances. It will read the instance by the given `instanceId` and then stop the instance if it's in a running state.

# Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class NightynightStack(Stack):

    def __init__(self, scope, id, props):
        super().__init__(scope, id, props)

        # The code that defines your stack goes here
        NightyNight(self, "nighty-night", instance_id="i-123123123123")
```

This will stop the instance with id `i-123123123123` at (the default) 4am GMT.

## Contributing

Please open Pull Requests and Issues on the [Github Repo](https://github.com/mbonig/nightynight).

## License

MIT
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_events
import aws_cdk.core


class NightyNight(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@matthewbonig/nightynight.NightyNight",
):
    """A construct that will build a Lambda and a CloudWatch Rule (cron schedule) that will stop the given ec2 instance at the specified time.

    Typically used when you've got ec2 instances that you only need during business hours
    and want to reduce the costs of.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: str,
        *,
        instance_id: str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param instance_id: the instanceId of the EC2 instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        """
        props = NightyNightProps(instance_id=instance_id, schedule=schedule)

        jsii.create(NightyNight, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@matthewbonig/nightynight.NightyNightProps",
    jsii_struct_bases=[],
    name_mapping={"instance_id": "instanceId", "schedule": "schedule"},
)
class NightyNightProps:
    def __init__(
        self,
        *,
        instance_id: str,
        schedule: typing.Optional[aws_cdk.aws_events.CronOptions] = None,
    ) -> None:
        """
        :param instance_id: the instanceId of the EC2 instance you'd like stopped.
        :param schedule: An option CronOptions to specify the time of day to stop the instance. Default: { day: '*', hour: '4', minute: '0' }
        """
        if isinstance(schedule, dict):
            schedule = aws_cdk.aws_events.CronOptions(**schedule)
        self._values = {
            "instance_id": instance_id,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def instance_id(self) -> str:
        """the instanceId of the EC2 instance you'd like stopped."""
        return self._values.get("instance_id")

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.CronOptions]:
        """An option CronOptions to specify the time of day to stop the instance.

        default
        :default:

        {
        day: '*',
        hour: '4',
        minute: '0'
        }
        """
        return self._values.get("schedule")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NightyNightProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NightyNight",
    "NightyNightProps",
]

publication.publish()
