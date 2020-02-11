from app.blueprints.projects import projects

from flask import current_app, render_template, redirect, url_for, flash, session
from flask_login import login_required


from app.blueprints.projects.stripe import stripeProductsList, convert_price
import requests, stripe 


@projects.route('/ecommerce')
@login_required
def ecommerce():
    try:
        if not session['cart']:
            pass
    except:
        session['cart'] = list()
    context ={
        'products':stripeProductsList
    }
    return render_template('ecommerce.html', **context)

@projects.route('/ecommerce/cart')
@login_required
def ecommerceCart():
    try:
        if not session['cart']:
            pass
    except:
        session['cart'] = list()
    print(stripeProductsList[0])
    context ={
        'products':stripeProductsList
    }
    return render_template('ecommerce-cart.html', **context)

@projects.route('/ecommerce/cart/add/product/<id>')
@login_required
def ecommerceCartAdd(id):
    p= stripe.SKU.retrieve(id)
    product = dict(
        id=p.id,
        prod_id=p.product,
        name=p.attributes.name,
        image=p.image,
        price=convert_price(p.price)
    )
    session['cart'].append(product)
    print(session['cart'])
    flash(f"[{product['name']}] added to your shopping cart","info")
    
    return redirect(url_for('projects.ecommerce'))