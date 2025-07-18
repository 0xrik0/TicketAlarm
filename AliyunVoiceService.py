# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_dyvmsapi20170525.client import Client as Dyvmsapi20170525Client
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dyvmsapi20170525 import models as dyvmsapi_20170525_models
from alibabacloud_credentials.models import Config as CredConfig
from alibabacloud_sts20150401.client import Client as Sts20150401Client
from alibabacloud_sts20150401.models import AssumeRoleRequest
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.models import RuntimeOptions
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_openapi.models import Config as OpenConfig


class VoiceService:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dyvmsapi20170525Client:
        sts_config = OpenConfig(
            access_key_id=os.getenv('STS_ACCESS_KEY_ID'),
            access_key_secret=os.getenv('STS_ACCESS_KEY_SECRET'),
        )
        sts_config.endpoint = "sts.aliyuncs.com"
        stsClient = Sts20150401Client(sts_config)

        assume_role_request = AssumeRoleRequest(
            # 会话有效时间
            duration_seconds=14400,
            # 要扮演的RAM角色ARN，示例值：acs:ram::123456789012****:role/adminrole，可以通过环境变量ALIBABA_CLOUD_ROLE_ARN设置role_arn
            role_arn=os.getenv('STS_ROLE_ARN'),
            # 角色会话名称，可以通过环境变量ALIBABA_CLOUD_ROLE_SESSION_NAME设置role_session_name
            role_session_name=os.getenv('STS_ROLE_SESSION_NAME'),
        )
        runtime = RuntimeOptions()
        try:
            resp = stsClient.assume_role_with_options(assume_role_request, runtime)
            assumeRoleResponseBodyCredentials = resp.body.credentials
            cred_cfg = CredConfig(
                type="sts",
                access_key_id=assumeRoleResponseBodyCredentials.access_key_id,
                access_key_secret=assumeRoleResponseBodyCredentials.access_key_secret,
                security_token=assumeRoleResponseBodyCredentials.security_token,
            )
            credential = CredentialClient(cred_cfg)
            config = open_api_models.Config(
                credential=credential
            )
            config.endpoint = f'dyvmsapi.aliyuncs.com'
            return Dyvmsapi20170525Client(config)
        except Exception as err:
            print(err)

    @staticmethod
    def main(DialNumber):
        client = VoiceService.create_client()
        single_call_by_tts_request = dyvmsapi_20170525_models.SingleCallByTtsRequest(
            called_number=f'{DialNumber}',
            tts_code='TTS_322455017' #写申请好的语音模板
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            result = client.single_call_by_tts_with_options(single_call_by_tts_request, runtime)
            status_code = result.body.code
            RequestId = result.body.request_id
            CallIdID = result.body.call_id
            return f"电话成功拨出，status_code{status_code}, RequestId{RequestId}, CallIdID{CallIdID}"
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

if __name__ == '__main__':
    #测试用，最终用户无需在意
    DialNumber = "" #写手机号
    VoiceService.main(DialNumber)
