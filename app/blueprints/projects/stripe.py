import stripe 
import os
from flask import current_app 
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

stripe.api_key = os.environ.get('STRIPE_API_KEY')

convert_price = lambda n: float(n/100)

stripeProductsList = [
    dict(
        id=p.id,
        prod_id=p.product,
        name=p.attributes.name,
        image=p.image,
        price=convert_price(p.price)
    )
    for p in stripe.SKU.list().data
    ]
