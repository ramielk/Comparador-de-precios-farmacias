import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session
from pharmacy_data import get_pharmacy_data, get_product_by_id, get_categories, filter_products

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key_for_development")

# ---- Carrito de compras ----
def add_to_cart(product_id, pharmacy_id):
    cart = session.get('cart', {})
    key = f'{pharmacy_id}:{product_id}'
    if key in cart:
        cart[key] += 1
    else:
        cart[key] = 1
    session['cart'] = cart

def remove_from_cart(product_id, pharmacy_id):
    cart = session.get('cart', {})
    key = f'{pharmacy_id}:{product_id}'
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
    session['cart'] = cart
    
# Main route - displays both pharmacies  
@app.route('/')
def index():
    pharmacy_data = get_pharmacy_data()
    return render_template('index.html', 
                          pharmacy1=pharmacy_data['pharmacy1'],
                          pharmacy2=pharmacy_data['pharmacy2'],
                          active_page='home')

# Individual pharmacy view
@app.route('/pharmacy/<pharmacy_id>')
def pharmacy(pharmacy_id):
    pharmacy_data = get_pharmacy_data()
    
    # Validate pharmacy_id
    if pharmacy_id not in ['pharmacy1', 'pharmacy2']:
        return redirect(url_for('index'))
    
    # Get filter parameters
    category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    availability = request.args.get('availability', '')
    
    # Get pharmacy data
    pharmacy = pharmacy_data[pharmacy_id]
    
    # Get all categories for filter dropdown
    categories = get_categories(pharmacy_data)
    
    # Filter products if needed
    if category or search_query or availability:
        pharmacy['products'] = filter_products(
            pharmacy['products'], 
            category=category,
            search_query=search_query,
            availability=availability
        )
    
    return render_template('pharmacy.html', 
                          pharmacy=pharmacy,
                          pharmacy_id=pharmacy_id,
                          categories=categories,
                          selected_category=category,
                          search_query=search_query,
                          selected_availability=availability,
                          active_page=pharmacy_id)
@app.route('/add_to_cart/<pharmacy_id>/<product_id>', methods=['POST'])
def add_cart_route(pharmacy_id, product_id):
    add_to_cart(product_id, pharmacy_id)
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_cart/<pharmacy_id>/<product_id>', methods=['POST'])
def remove_cart_route(pharmacy_id, product_id):
    remove_from_cart(product_id, pharmacy_id)
    return redirect(request.referrer or url_for('index'))

# Product comparison route
@app.route('/compare')
def compare():
    pharmacy_data = get_pharmacy_data()
    
    # Get product IDs from query parameters
    product1_id = request.args.get('product1')
    product2_id = request.args.get('product2')
    
    # Get pharmacy IDs
    pharmacy1_id = request.args.get('pharmacy1', 'pharmacy1')
    pharmacy2_id = request.args.get('pharmacy2', 'pharmacy2')
    
    # Validate pharmacy IDs
    if pharmacy1_id not in ['pharmacy1', 'pharmacy2'] or pharmacy2_id not in ['pharmacy1', 'pharmacy2']:
        return redirect(url_for('index'))
    
    # Get product details
    product1 = get_product_by_id(pharmacy_data[pharmacy1_id]['products'], product1_id) if product1_id else None
    product2 = get_product_by_id(pharmacy_data[pharmacy2_id]['products'], product2_id) if product2_id else None
    
    return render_template('compare.html', 
                          product1=product1,
                          product2=product2,
                          pharmacy1=pharmacy_data[pharmacy1_id],
                          pharmacy2=pharmacy_data[pharmacy2_id],
                          pharmacy1_id=pharmacy1_id,
                          pharmacy2_id=pharmacy2_id,
                          active_page='compare')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
