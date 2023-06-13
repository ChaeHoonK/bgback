import boto3

client = boto3.client('cognito-idp', region_name='us-west-2')


def user_sign_up(username, password, email):
    response = client.sign_up(
        ClientId='APP_CLIENT_ID',   # replace with your app client id
        Username=username,        # replace with the user's username
        Password=password,        # replace with the user's password
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
        ],
        ConfirmationDeliveryMedium='EMAIL',
    )

## Authentication
def user_auth(username, password):
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password,
        },
        ClientId='APP_CLIENT_ID',
    )

    # The response contains Access, ID, and Refresh tokens.
    tokens = response['AuthenticationResult']


## Token Refresh

def user_refresh_token(app_client_id):
    response = client.initiate_auth(
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': 'RefreshToken',
        },
        ClientId=app_client_id,
    )

    # The new tokens are in the response
    tokens = response['AuthenticationResult']
