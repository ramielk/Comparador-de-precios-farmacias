import logging
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pharmacy_data import get_pharmacy_data, get_product_by_id, get_categories, filter_products

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SESSION_SECRET", "una_clave_secreta_muy_dificil_de_adivinar_12345")

# ---- Carrito de compras - Funciones de lógica ----
def add_to_cart_logic(product_id, pharmacy_id):
    cart = session.get('cart', {})
    key = f'{pharmacy_id}:{product_id}'
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    logging.debug(f"Producto {product_id} de farmacia {pharmacy_id} agregado. Carrito: {cart}")

def remove_from_cart_logic(product_id, pharmacy_id):
    cart = session.get('cart', {})
    key = f'{pharmacy_id}:{product_id}'
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
        session['cart'] = cart
        logging.debug(f"Producto {product_id} de farmacia {pharmacy_id} removido. Carrito: {cart}")
    else:
        logging.debug(f"Intento de remover producto {product_id} de farmacia {pharmacy_id} que no está en el carrito.")

def get_total_cart_items():
    cart = session.get('cart', {})
    return sum(cart.values())

# Main route - displays both pharmacies  
@app.route('/')
def index():
    pharmacy_data = get_pharmacy_data()
    total_cart_items = get_total_cart_items() 
    return render_template('index.html', 
                            pharmacy1=pharmacy_data['pharmacy1'],
                            pharmacy2=pharmacy_data['pharmacy2'],
                            active_page='home',
                            total_cart_items=total_cart_items)

# Individual pharmacy view
@app.route('/pharmacy/<pharmacy_id>')
def pharmacy(pharmacy_id):
    pharmacy_data = get_pharmacy_data()
    
    if pharmacy_id not in ['pharmacy1', 'pharmacy2']:
        flash('Farmacia no encontrada.', 'error')
        return redirect(url_for('index'))
    
    category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    availability = request.args.get('availability', '')
    
    pharmacy = pharmacy_data[pharmacy_id]
    
    categories = get_categories(pharmacy_data)
    
    original_products = pharmacy['products'] 
    
    if category or search_query or availability:
        pharmacy['products'] = filter_products(
            original_products,
            category=category,
            search_query=search_query,
            availability=availability
        )
    
    total_cart_items = get_total_cart_items()

    return render_template('pharmacy.html', 
                            pharmacy=pharmacy,
                            pharmacy_id=pharmacy_id,
                            categories=categories,
                            selected_category=category,
                            search_query=search_query,
                            selected_availability=availability,
                            active_page=pharmacy_id,
                            total_cart_items=total_cart_items)

# Rutas del carrito
@app.route('/add_to_cart/<pharmacy_id>/<product_id>', methods=['POST'])
def add_cart_route(pharmacy_id, product_id):
    pharmacy_data = get_pharmacy_data()
    product_info = None
    if pharmacy_id in pharmacy_data:
        for p in pharmacy_data[pharmacy_id]['products']:
            if str(p['id']) == product_id:
                product_info = p
                break

    if product_info:
        add_to_cart_logic(product_id, pharmacy_id)
        flash(f"'{product_info['name']}' de {pharmacy_data[pharmacy_id]['name']} agregado al carrito.", 'success')
    else:
        flash("Error al agregar el producto al carrito.", 'error')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_cart/<pharmacy_id>/<product_id>', methods=['POST'])
def remove_cart_route(pharmacy_id, product_id):
    pharmacy_data = get_pharmacy_data()
    product_info = None
    if pharmacy_id in pharmacy_data:
        for p in pharmacy_data[pharmacy_id]['products']:
            if str(p['id']) == product_id:
                product_info = p
                break
    
    cart = session.get('cart', {})
    key = f'{pharmacy_id}:{product_id}'

    if key in cart and cart[key] > 0:
        remove_from_cart_logic(product_id, pharmacy_id)
        flash(f"'{product_info['name']}' de {pharmacy_data[pharmacy_id]['name']} removido del carrito.", 'info')
    else:
        flash("El producto no está en tu carrito o ya no tienes unidades para remover.", 'warning')

    return redirect(request.referrer or url_for('index'))

# --- NUEVA RUTA PARA VER EL CARRITO (CAMBIO PRINCIPAL) ---
@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    pharmacy_data = get_pharmacy_data()
    cart_items_details = []
    total_price = 0

    for key, quantity in cart.items():
        pharmacy_id, product_id = key.split(':')
        
        # Asegurarse de que pharmacy_id es válido
        if pharmacy_id in pharmacy_data:
            product = get_product_by_id(pharmacy_data[pharmacy_id]['products'], product_id)
            if product:
                item_total = product['price'] * quantity
                total_price += item_total
                cart_items_details.append({
                    'pharmacy_id': pharmacy_id,
                    'pharmacy_name': pharmacy_data[pharmacy_id]['name'],
                    'product_id': product_id,
                    'product_name': product['name'],
                    'quantity': quantity,
                    'price': product['price'],
                    'item_total': item_total
                })
            else:
                flash(f"Error: Producto con ID {product_id} no encontrado en {pharmacy_data[pharmacy_id]['name']}. Podría haber sido eliminado.", 'error')
                # Opcional: remover el ítem del carrito si el producto ya no existe
                # del session['cart'][key] 
        else:
            flash(f"Error: Farmacia con ID {pharmacy_id} no encontrada para un ítem del carrito.", 'error')
            # Opcional: remover el ítem del carrito si la farmacia ya no existe
            # del session['cart'][key]

    total_cart_items = get_total_cart_items() # Para el contador en el layout
    return render_template('cart.html', 
                           cart_items=cart_items_details, 
                           total_price=total_price,
                           total_cart_items=total_cart_items, # Variable para el layout
                           active_page='cart') # Para que el menú se resalte

# Product comparison route
@app.route('/compare')
def compare():
    pharmacy_data = get_pharmacy_data()
    
    product1_id = request.args.get('product1')
    product2_id = request.args.get('product2')
    
    pharmacy1_id = request.args.get('pharmacy1', 'pharmacy1')
    pharmacy2_id = request.args.get('pharmacy2', 'pharmacy2')
    
    if pharmacy1_id not in ['pharmacy1', 'pharmacy2'] or pharmacy2_id not in ['pharmacy1', 'pharmacy2']:
        flash('IDs de farmacia inválidos para la comparación.', 'error')
        return redirect(url_for('index'))
    
    product1 = get_product_by_id(pharmacy_data[pharmacy1_id]['products'], product1_id) if product1_id else None
    product2 = get_product_by_id(pharmacy_data[pharmacy2_id]['products'], product2_id) if product2_id else None
    
    total_cart_items = get_total_cart_items()

    return render_template('compare.html', 
                            product1=product1,
                            product2=product2,
                            pharmacy1=pharmacy_data[pharmacy1_id],
                            pharmacy2=pharmacy_data[pharmacy2_id],
                            pharmacy1_id=pharmacy1_id,
                            pharmacy2_id=pharmacy2_id,
                            active_page='compare',
                            total_cart_items=total_cart_items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

