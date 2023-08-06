import boto3
from RDS_Cognito_attribute_alignment.rds_cognito_pkg.settings import COGNITO_ATTRIBUTE

client = boto3.client('cognito-idp', region_name=region)


class User:
    """
    This class defines an actual user.
    """
    user_pool_id = 'us-east-1_Hx4y8Olmh'

    def __init__(self, user_id, rds_value):
        self.user_id = user_id
        self.rds_value = rds_value
        self.cognito_value = ''

    def get_cognito_attr_value(self):
        """
        Use this function to connect to Cognito and retrieve a specific user attribute value.
        """
        response = client.admin_get_user(
            UserPoolId=self.user_pool_id,
            Username=self.user_id
        )
        user_attributes = response['UserAttributes']

        for attribute in user_attributes:
            if attribute['Name'] == COGNITO_ATTRIBUTE:
                self.cognito_value = attribute['Value']

    def rds_cognito_match(self):
        """
        Use this function to verify whether or not RDS and Cognito attribute values match
        """
        return str(self.rds_value) == str(self.cognito_value)