"""
# AWS Budget Notifier

Setup AWS Budget notifications using AWS CDK.
By default notifications are sent to all subscribers via e-mail.

## Example usage

```javascript
import * as cdk from "@aws-cdk/core";

import { CfnBudget } from "@aws-cdk/aws-budgets";
import { StackProps } from "@aws-cdk/core";
import { BudgetNotifier } from "./budget_notifier";

export class BudgetNotifierStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new BudgetNotifier(this, "test", {
      recipients: ["john@doe.com"],
      availabilityZones: ["eu-central-1", "eu-west-1"],
      application: "HelloWorld",
      costCenter: "myCostCenter",
      limit: 10,
      unit: "USD",
      threshold: 75,
    });
  }
}
```

## Links

* [API documentation](./API.md)
* [AWS Cloud Development Kit (CDK)](https://github.com/aws/aws-cdk)
* [Cost Explorer filters](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-filtering.html)
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

import aws_cdk.core


class BudgetNotifier(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@stefanfreitag/aws-budget-notifier.BudgetNotifier",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        limit: jsii.Number,
        recipients: typing.List[builtins.str],
        threshold: jsii.Number,
        unit: builtins.str,
        application: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        cost_center: typing.Optional[builtins.str] = None,
        notification_type: typing.Optional["NotificationType"] = None,
        service: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional["TimeUnit"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param limit: The cost associated with the budget threshold.
        :param recipients: Budget notifications will be sent to each of the recipients (e-mail addresses).
        :param threshold: The threshold value in percent (0-100).
        :param unit: The unit of measurement that is used for the budget threshold, such as dollars or GB.
        :param application: If specified the application name will be added as tag filter.
        :param availability_zones: If specified the availability zones will be added as tag filter.
        :param cost_center: If specified the cost center will be added as tag filter.
        :param notification_type: Whether the notification is for how much you have spent (ACTUAL) or for how much you're forecasted to spend (FORECASTED).
        :param service: If specified the service will be added as tag filter.
        :param time_unit: The length of time until a budget resets the actual and forecasted spend.

        stability
        :stability: experimental
        """
        props = BudgetNotifierProps(
            limit=limit,
            recipients=recipients,
            threshold=threshold,
            unit=unit,
            application=application,
            availability_zones=availability_zones,
            cost_center=cost_center,
            notification_type=notification_type,
            service=service,
            time_unit=time_unit,
        )

        jsii.create(BudgetNotifier, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@stefanfreitag/aws-budget-notifier.BudgetNotifierProps",
    jsii_struct_bases=[],
    name_mapping={
        "limit": "limit",
        "recipients": "recipients",
        "threshold": "threshold",
        "unit": "unit",
        "application": "application",
        "availability_zones": "availabilityZones",
        "cost_center": "costCenter",
        "notification_type": "notificationType",
        "service": "service",
        "time_unit": "timeUnit",
    },
)
class BudgetNotifierProps:
    def __init__(
        self,
        *,
        limit: jsii.Number,
        recipients: typing.List[builtins.str],
        threshold: jsii.Number,
        unit: builtins.str,
        application: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        cost_center: typing.Optional[builtins.str] = None,
        notification_type: typing.Optional["NotificationType"] = None,
        service: typing.Optional[builtins.str] = None,
        time_unit: typing.Optional["TimeUnit"] = None,
    ) -> None:
        """
        :param limit: The cost associated with the budget threshold.
        :param recipients: Budget notifications will be sent to each of the recipients (e-mail addresses).
        :param threshold: The threshold value in percent (0-100).
        :param unit: The unit of measurement that is used for the budget threshold, such as dollars or GB.
        :param application: If specified the application name will be added as tag filter.
        :param availability_zones: If specified the availability zones will be added as tag filter.
        :param cost_center: If specified the cost center will be added as tag filter.
        :param notification_type: Whether the notification is for how much you have spent (ACTUAL) or for how much you're forecasted to spend (FORECASTED).
        :param service: If specified the service will be added as tag filter.
        :param time_unit: The length of time until a budget resets the actual and forecasted spend.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "limit": limit,
            "recipients": recipients,
            "threshold": threshold,
            "unit": unit,
        }
        if application is not None:
            self._values["application"] = application
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cost_center is not None:
            self._values["cost_center"] = cost_center
        if notification_type is not None:
            self._values["notification_type"] = notification_type
        if service is not None:
            self._values["service"] = service
        if time_unit is not None:
            self._values["time_unit"] = time_unit

    @builtins.property
    def limit(self) -> jsii.Number:
        """The cost associated with the budget threshold.

        stability
        :stability: experimental
        """
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return result

    @builtins.property
    def recipients(self) -> typing.List[builtins.str]:
        """Budget notifications will be sent to each of the recipients (e-mail addresses).

        stability
        :stability: experimental
        """
        result = self._values.get("recipients")
        assert result is not None, "Required property 'recipients' is missing"
        return result

    @builtins.property
    def threshold(self) -> jsii.Number:
        """The threshold value in percent (0-100).

        stability
        :stability: experimental
        """
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return result

    @builtins.property
    def unit(self) -> builtins.str:
        """The unit of measurement that is used for the budget threshold, such as dollars or GB.

        stability
        :stability: experimental
        """
        result = self._values.get("unit")
        assert result is not None, "Required property 'unit' is missing"
        return result

    @builtins.property
    def application(self) -> typing.Optional[builtins.str]:
        """If specified the application name will be added as tag filter.

        stability
        :stability: experimental
        """
        result = self._values.get("application")
        return result

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        """If specified the availability zones will be added as tag filter.

        stability
        :stability: experimental
        """
        result = self._values.get("availability_zones")
        return result

    @builtins.property
    def cost_center(self) -> typing.Optional[builtins.str]:
        """If specified the cost center will be added as tag filter.

        stability
        :stability: experimental
        """
        result = self._values.get("cost_center")
        return result

    @builtins.property
    def notification_type(self) -> typing.Optional["NotificationType"]:
        """Whether the notification is for how much you have spent (ACTUAL) or for how much you're forecasted to spend (FORECASTED).

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-notificationtype
        stability
        :stability: experimental
        """
        result = self._values.get("notification_type")
        return result

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        """If specified the service will be added as tag filter.

        stability
        :stability: experimental
        """
        result = self._values.get("service")
        return result

    @builtins.property
    def time_unit(self) -> typing.Optional["TimeUnit"]:
        """The length of time until a budget resets the actual and forecasted spend.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-timeunit
        stability
        :stability: experimental
        """
        result = self._values.get("time_unit")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetNotifierProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@stefanfreitag/aws-budget-notifier.NotificationType")
class NotificationType(enum.Enum):
    """
    stability
    :stability: experimental
    """

    ACTUAL = "ACTUAL"
    """
    stability
    :stability: experimental
    """
    FORECASTED = "FORECASTED"
    """
    stability
    :stability: experimental
    """


@jsii.enum(jsii_type="@stefanfreitag/aws-budget-notifier.TimeUnit")
class TimeUnit(enum.Enum):
    """
    stability
    :stability: experimental
    """

    MONTHLY = "MONTHLY"
    """
    stability
    :stability: experimental
    """
    QUARTERLY = "QUARTERLY"
    """
    stability
    :stability: experimental
    """
    ANNUALLY = "ANNUALLY"
    """
    stability
    :stability: experimental
    """


__all__ = [
    "BudgetNotifier",
    "BudgetNotifierProps",
    "NotificationType",
    "TimeUnit",
]

publication.publish()
