from app.blueprints.projects import projects

from flask import current_app, render_template, redirect, url_for, flash, session
from flask_login import login_required


from app.blueprints.projects.stripe import stripeProductsList, convert_price, initProducts
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
    shallowCart = []
    for i in session['cart']:
      if i not in shallowCart:
        shallowCart.append(i)
    for i in shallowCart:
      i['quantity'] = session['cart'].count(i)
  except:
    session['cart'] = list()
    initProducts()
  context = {
    'products': initProducts(),
    'cart': session['cart'],
    'shallowCart': shallowCart,
    'grandTotal': round(sum([i['price'] for i in session['cart']]), 2),
    'round': round
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

@projects.route('/ecommerce/cart/clear')
@login_required
def ecommerceCartClear():
  if session['cart']:
    session['cart'] = list()
    flash("You have cleared all items from your cart.", "info")
  else:
    flash("You cannot clear items from a cart you don't have.", "warning")
  return redirect(url_for('projects.ecommerceCart'))

@projects.route('/ecommerce/cart/remove/<id>')
@login_required
def ecommerceCartRemove(id):
  product = stripe.SKU.retrieve(id)
  try:
    for i in session['cart']:
      if product['id'] == i['id']:
        session['cart'].remove(i)
        flash(f"You have removed {product.attributes.name}.", "info")
        break
  except:
    flash(f"{product.attributes.name} could not be removed", "warning")
  return redirect(url_for('projects.ecommerceCart'))