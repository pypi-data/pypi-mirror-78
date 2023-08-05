import boto3
from vulcan.aws.services._session import AWSSession


class AWSLogs(AWSSession):

    def __init__(self, **kwargs):
        super(
            self.__class__,
            self
        ).__init__(kwargs['profile_name'], kwargs.get('region_name', None))

    def group_exists(self, **kwargs):
        if 'group_name' not in kwargs:
            raise Exception('Argument missing: group_name')

        resp = self.client('logs').describe_log_groups(
            logGroupNamePrefix=kwargs.get('group_name')
        )

        result = False
        for group in resp['logGroups']:
            if group['logGroupName'] == kwargs['group_name']:
                result = True

        return result
