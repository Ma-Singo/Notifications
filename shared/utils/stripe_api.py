import stripe

from core.config import Settings

stripe.api_key = Settings.stripe_key

# TODO: change dict to User class
def create_customer(user:  dict) -> dict:
    return stripe.Customer.create(
        name=user.get('name'),
        email=user.get('email'),
    )
