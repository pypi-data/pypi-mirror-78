import boto3


class DeployModel(object):

    def deploy_to_s3(self, model_version):
        s3_resource = boto3.resource('s3')
        bucket_name = 'category-model' if 'category_model' in model_version.split('/') else 'food-model'

        print('Uploading {} to Amazon S3 bucket {}'.format(model_version, bucket_name))
        s3_resource.Object(bucket_name, model_version.split('/')[-1]).put(
            Body=open(model_version, 'rb'), ACL='public-read')
