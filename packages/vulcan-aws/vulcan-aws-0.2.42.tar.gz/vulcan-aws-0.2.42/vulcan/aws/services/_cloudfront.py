import uuid
from vulcan.aws.services._session import AWSSession


class AWSCloudFront(AWSSession):

    def __init__(self, **kwargs):
        super(
            self.__class__,
            self
        ).__init__(kwargs['profile_name'], kwargs.get('region_name', None))

        self.distribution_id = kwargs.get('distribution_id')

    def invalidate(self, *files):
        cloudfront = self.client('cloudfront')
        resp = cloudfront.create_invalidation(
            DistributionId=self.distribution_id,
            InvalidationBatch={
                'CallerReference': uuid.uuid4().hex,
                'Paths': {
                    'Quantity': len(files),
                    'Items': files
                }
            }
        )
