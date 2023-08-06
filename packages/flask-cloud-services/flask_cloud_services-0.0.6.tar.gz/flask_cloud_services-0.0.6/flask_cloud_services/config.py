import os

PROVIDER = os.environ.get('CLOUD_SERVICES_PROVIDER')

# AWS Config
AWS_REGION = os.environ.get('CLOUD_SERVICES_AWS_REGION')
AWS_ACCESS_KEY = os.environ.get('CLOUD_SERVICES_AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('CLOUD_SERVICES_AWS_SECRET_KEY')

# Notification Bus services
NOTIFICATION = 'Notification'
SUSCRIPTION = 'Subscription'
