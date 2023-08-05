# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from . import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Domain']


class Domain(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 smtp_password: Optional[pulumi.Input[str]] = None,
                 spam_action: Optional[pulumi.Input[str]] = None,
                 wildcard: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a Mailgun App resource. This can be used to
        create and manage applications on Mailgun.

        After DNS records are set, domain verification should be triggered manually using [PUT /domains/\<domain\>/verify](https://documentation.mailgun.com/en/latest/api-domains.html#domains)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_mailgun as mailgun

        # Create a new Mailgun domain
        default = mailgun.Domain("default",
            region="us",
            smtp_password="supersecretpassword1234",
            spam_action="disabled")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The domain to add to Mailgun
        :param pulumi.Input[str] region: The region where domain will be created. Default value is `us`.
        :param pulumi.Input[str] smtp_password: Password for SMTP authentication
        :param pulumi.Input[str] spam_action: `disabled` or `tag` Disable, no spam
               filtering will occur for inbound messages. Tag, messages
               will be tagged with a spam header.
        :param pulumi.Input[bool] wildcard: Boolean that determines whether
               the domain will accept email for sub-domains.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['name'] = name
            __props__['region'] = region
            __props__['smtp_password'] = smtp_password
            __props__['spam_action'] = spam_action
            __props__['wildcard'] = wildcard
            __props__['receiving_records'] = None
            __props__['sending_records'] = None
            __props__['smtp_login'] = None
        super(Domain, __self__).__init__(
            'mailgun:index/domain:Domain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            receiving_records: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DomainReceivingRecordArgs']]]]] = None,
            region: Optional[pulumi.Input[str]] = None,
            sending_records: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DomainSendingRecordArgs']]]]] = None,
            smtp_login: Optional[pulumi.Input[str]] = None,
            smtp_password: Optional[pulumi.Input[str]] = None,
            spam_action: Optional[pulumi.Input[str]] = None,
            wildcard: Optional[pulumi.Input[bool]] = None) -> 'Domain':
        """
        Get an existing Domain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The domain to add to Mailgun
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DomainReceivingRecordArgs']]]] receiving_records: A list of DNS records for receiving validation.
        :param pulumi.Input[str] region: The region where domain will be created. Default value is `us`.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DomainSendingRecordArgs']]]] sending_records: A list of DNS records for sending validation.
        :param pulumi.Input[str] smtp_login: The login email for the SMTP server.
        :param pulumi.Input[str] smtp_password: Password for SMTP authentication
        :param pulumi.Input[str] spam_action: `disabled` or `tag` Disable, no spam
               filtering will occur for inbound messages. Tag, messages
               will be tagged with a spam header.
        :param pulumi.Input[bool] wildcard: Boolean that determines whether
               the domain will accept email for sub-domains.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["name"] = name
        __props__["receiving_records"] = receiving_records
        __props__["region"] = region
        __props__["sending_records"] = sending_records
        __props__["smtp_login"] = smtp_login
        __props__["smtp_password"] = smtp_password
        __props__["spam_action"] = spam_action
        __props__["wildcard"] = wildcard
        return Domain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The domain to add to Mailgun
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="receivingRecords")
    def receiving_records(self) -> List['outputs.DomainReceivingRecord']:
        """
        A list of DNS records for receiving validation.
        """
        return pulumi.get(self, "receiving_records")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        """
        The region where domain will be created. Default value is `us`.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="sendingRecords")
    def sending_records(self) -> List['outputs.DomainSendingRecord']:
        """
        A list of DNS records for sending validation.
        """
        return pulumi.get(self, "sending_records")

    @property
    @pulumi.getter(name="smtpLogin")
    def smtp_login(self) -> str:
        """
        The login email for the SMTP server.
        """
        return pulumi.get(self, "smtp_login")

    @property
    @pulumi.getter(name="smtpPassword")
    def smtp_password(self) -> Optional[str]:
        """
        Password for SMTP authentication
        """
        return pulumi.get(self, "smtp_password")

    @property
    @pulumi.getter(name="spamAction")
    def spam_action(self) -> Optional[str]:
        """
        `disabled` or `tag` Disable, no spam
        filtering will occur for inbound messages. Tag, messages
        will be tagged with a spam header.
        """
        return pulumi.get(self, "spam_action")

    @property
    @pulumi.getter
    def wildcard(self) -> Optional[bool]:
        """
        Boolean that determines whether
        the domain will accept email for sub-domains.
        """
        return pulumi.get(self, "wildcard")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

