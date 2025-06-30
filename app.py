from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
    abort # Import abort for 403 errors
)
from forms import RegistrationForm, LoginForm
from models import db, Pharmacy, Product, User, Order, OrderItem, Payment
from datetime import datetime # Import datetime

import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)



# ======================================================================
# CONFIGURACIÓN DE SEGURIDAD PRINCIPAL
# ======================================================================

# Configuración de seguridad - CLAVE SECRETA
app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET", "super-secret-key-default-for-dev") # Added a default for dev

print(
    "Clave secreta configurada correctamente."
    if app.config["SECRET_KEY"]
    else "Error: No se pudo configurar la clave secreta."
)

# Configuración de cookies seguras para protección adicional
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE="Lax",  # Protection against CSRF
    PERMANENT_SESSION_LIFETIME=3600,  # 1 hour session duration
)

# Configurar la clave secreta para las sesiones (redundant with app.config["SECRET_KEY"] but harmless)
app.secret_key = os.environ.get("SESSION_SECRET", "clave-secreta-predeterminada")

# Habilitar protección CSRF global
csrf = CSRFProtect()
csrf.init_app(app)


# Configurar cabeceras de seguridad HTTP con Flask-Talisman
Talisman(
    app,
    content_security_policy={
        "default-src": "'self'",
        "style-src": ["'self'", "https://cdn.jsdelivr.net", "'unsafe-inline'"],
        "script-src": ["'self'", "https://cdn.jsdelivr.net", "'unsafe-inline'"], # Allow inline scripts for now, consider nonces
        "font-src": ["'self'", "https://cdn.jsdelivr.net", "data:"],
        "img-src": [
            "'self'",
            "data:",
            "https://somoscomunidad.org.ve",
            "https://farmahorro.com.ve",
            "https://placehold.co", # Added for placeholder images
        ],
    },
    # content_security_policy_nonce_in=["script-src"], # Uncomment if using nonces in scripts
    frame_options="SAMEORIGIN",
    strict_transport_security=True,
    force_https=False,  # Set to True in production with HTTPS
    session_cookie_http_only=True,
    session_cookie_secure=True, # Set to True in production with HTTPS
)

# Configurar protección contra fuerza bruta con Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# ======================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ======================================================================

# Configuración de base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  # Inicializar la extensión con la app

# Configuración de login
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Cargador de usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ======================================================================
# FUNCIONALIDAD DE LA APLICACIÓN
# ======================================================================

# Crear tablas en la base de datos SOLO si no existen
with app.app_context():
    db.create_all()
    # Optional: Add an accountant user for testing if none exists
    if not User.query.filter_by(email='accountant@example.com').first():
        hashed_password = generate_password_hash('password') # Use a strong password in production
        accountant_user = User(username='accountant', email='accountant@example.com', password=hashed_password, role='accountant')
        db.session.add(accountant_user)
        db.session.commit()
        logging.info("Accountant user created: accountant@example.com / password")

# ---- Carrito de compras - Funciones de lógica ----
def add_to_cart_logic(product_id, pharmacy_id):
    cart = session.get("cart", {})
    key = f"{pharmacy_id}:{product_id}"
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart
    logging.debug(
        f"Producto {product_id} de farmacia {pharmacy_id} agregado. Carrito: {cart}"
    )

def remove_from_cart_logic(product_id, pharmacy_id):
    cart = session.get("cart", {})
    key = f"{pharmacy_id}:{product_id}"
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
        session["cart"] = cart
        logging.debug(
            f"Producto {product_id} de farmacia {pharmacy_id} removido. Carrito: {cart}"
        )
    else:
        logging.debug(
            f"Intento de remover producto {product_id} de farmacia {pharmacy_id} que no está en el carrito."
        )

def get_total_cart_items():
    cart = session.get("cart", {})
    return sum(cart.values())

def clear_cart():
    session["cart"] = {}
    logging.debug("Carrito de la sesión vaciado.")

# ---- Funciones de utilidad para roles ----
def is_accountant():
    return current_user.is_authenticated and current_user.role == 'accountant'

def accountant_required(f):
    """Decorator to restrict access to accountant users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_accountant():
            flash('No tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

from functools import wraps # Import wraps for decorators

# ======================================================================
# RUTAS DE LA APLICACIÓN
# ======================================================================

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow} 

# Main route - displays both pharmacies
@app.route("/")
@login_required
def home():
    pharmacies = Pharmacy.query.all()
    return render_template(
        "index.html",
        pharmacies=pharmacies,
        active_page="home",
    )


@app.route("/pharmacy/<int:pharmacy_id>")
@login_required
def pharmacy(pharmacy_id):
    pharmacy = Pharmacy.query.get_or_404(pharmacy_id)
    category = request.args.get("category", "")
    search_query = request.args.get("search", "")
    availability = request.args.get("availability", "")
    products = pharmacy.products

    # Filtros
    if category:
        products = [p for p in products if p.category == category]
    if search_query:
        products = [
            p
            for p in products
            if search_query.lower() in p.name.lower()
            or search_query.lower() in p.description.lower()
        ]
    if availability == "in_stock":
        products = [p for p in products if p.in_stock]
    elif availability == "out_of_stock":
        products = [p for p in products if not p.in_stock]

    total_cart_items = get_total_cart_items()
    categories = sorted(
        list(set([p.category for p in pharmacy.products if p.category]))
    )

    # Pasa el product1_id si está en los argumentos de la URL
    product1_id = request.args.get("product1", type=int)
    product2_id = request.args.get("product2", type=int)

    return render_template(
        "pharmacy.html",
        pharmacy=pharmacy,
        products=products,
        categories=categories,
        selected_category=category,
        search_query=search_query,
        selected_availability=availability,
        total_cart_items=total_cart_items,
        product1_id=product1_id,
        product2_id=product2_id,
        pharmacy_id=pharmacy_id,
    )


# Rutas del carrito
@app.route("/add_to_cart/<int:pharmacy_id>/<int:product_id>", methods=["POST"])
@login_required
def add_cart_route(pharmacy_id, product_id):
    product = Product.query.filter_by(id=product_id, pharmacy_id=pharmacy_id).first()
    if product:
        add_to_cart_logic(product_id, pharmacy_id)
        flash(
            f"'{product.name}' de {product.pharmacy.name} agregado al carrito.",
            "success",
        )
    else:
        flash("Error al agregar el producto al carrito.", "error")
    return redirect(request.referrer or url_for("home"))


@app.route("/remove_from_cart/<int:pharmacy_id>/<int:product_id>", methods=["POST"])
@login_required
def remove_cart_route(pharmacy_id, product_id):
    product = Product.query.filter_by(id=product_id, pharmacy_id=pharmacy_id).first()
    cart = session.get("cart", {})
    key = f"{pharmacy_id}:{product_id}"
    if product and key in cart and cart[key] > 0:
        remove_from_cart_logic(product_id, pharmacy_id)
        flash(
            f"'{product.name}' de {product.pharmacy.name} removido del carrito.", "info"
        )
    else:
        flash(
            "El producto no está en tu carrito o ya no tienes unidades para remover.",
            "warning",
        )
    return redirect(request.referrer or url_for("home"))


@app.route("/cart")
@login_required
def view_cart():
    cart = session.get("cart", {})
    cart_items_details = []
    total_price = 0
    
    # Track if any product in cart is invalid
    invalid_product_in_cart = False

    for key, quantity in cart.items():
        pharmacy_id, product_id = map(int, key.split(":"))
        product = Product.query.filter_by(
            id=product_id, pharmacy_id=pharmacy_id
        ).first()
        if product:
            item_total = product.price * quantity
            total_price += item_total
            cart_items_details.append(
                {
                    "pharmacy_id": pharmacy_id,
                    "pharmacy_name": product.pharmacy.name,
                    "product_id": product_id,
                    "product_name": product.name,
                    "quantity": quantity,
                    "price": product.price,
                    "item_total": item_total,
                }
            )
        else:
            flash(
                f"Error: Producto con ID {product_id} no encontrado en la base de datos y ha sido removido del carrito.",
                "error",
            )
            invalid_product_in_cart = True
            # Remove invalid item from cart session to prevent persistent errors
            del session['cart'][key]
            session.modified = True # Important to mark session as modified after direct dict manipulation


    total_cart_items = get_total_cart_items()
    return render_template(
        "cart.html",
        cart_items=cart_items_details,
        total_price=total_price,
        total_cart_items=total_cart_items,
        active_page="cart",
        invalid_product_in_cart=invalid_product_in_cart # Pass flag to template
    )

# ---- Rutas de Checkout y Pago ----
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("Tu carrito está vacío. Agrega productos antes de proceder al pago.", "warning")
        return redirect(url_for("view_cart"))

    cart_items_details = []
    total_price = 0
    products_to_order = [] # To store actual Product objects for order creation

    for key, quantity in cart.items():
        pharmacy_id, product_id = map(int, key.split(":"))
        product = Product.query.filter_by(id=product_id, pharmacy_id=pharmacy_id).first()
        if not product or product.stock_quantity < quantity: # Basic stock check
            flash(f"Producto '{product.name}' de {product.pharmacy.name} no disponible en la cantidad solicitada o no existe. Por favor, revisa tu carrito.", "danger")
            return redirect(url_for("view_cart"))
        
        item_total = product.price * quantity
        total_price += item_total
        cart_items_details.append({
            "pharmacy_id": pharmacy_id,
            "pharmacy_name": product.pharmacy.name,
            "product_id": product_id,
            "product_name": product.name,
            "quantity": quantity,
            "price": product.price,
            "item_total": item_total,
        })
        products_to_order.append({"product": product, "quantity": quantity})


    if request.method == "POST":
        try:
            # Create a new Order
            new_order = Order(
                user_id=current_user.id,
                total_amount=total_price,
                status='payment_submitted' # Initial status after checkout confirmation
            )
            db.session.add(new_order)
            db.session.flush() # Get the ID for the new_order before committing

            # Add items to the order
            for item_data in products_to_order:
                product = item_data["product"]
                quantity = item_data["quantity"]
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    pharmacy_id=product.pharmacy_id,
                    quantity=quantity,
                    price_at_purchase=product.price
                )
                db.session.add(order_item)
                
                # Optionally, deduct stock here if you want to implement stock management
                # product.stock_quantity -= quantity
                # db.session.add(product) # Mark product as modified if its stock changes

            db.session.commit()
            clear_cart() # Empty the cart after creating the order
            flash(f"Tu pedido #{new_order.id} ha sido creado. Ahora, por favor, introduce los detalles de tu pago.", "success")
            return redirect(url_for("payment_form", order_id=new_order.id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al procesar el checkout: {e}", exc_info=True)
            flash("Ocurrió un error al procesar tu pedido. Inténtalo de nuevo.", "danger")
            return redirect(url_for("view_cart"))

    return render_template(
        "checkout.html",
        cart_items=cart_items_details,
        total_price=total_price,
        active_page="checkout"
    )

@app.route("/payment_form/<int:order_id>", methods=["GET", "POST"])
@login_required
def payment_form(order_id):
    order = Order.query.get_or_404(order_id)

    # Ensure the order belongs to the current user and is in the correct status
    if order.user_id != current_user.id:
        flash("No tienes permiso para acceder a esta orden.", "danger")
        return redirect(url_for("home"))
    
    if order.status not in ['pending', 'payment_submitted']:
        flash("Esta orden ya ha sido procesada o está en un estado no editable.", "warning")
        return redirect(url_for("invoice", order_id=order.id))

    if request.method == "POST":
        reference_number = request.form.get("reference_number").strip()
        if not reference_number:
            flash("Por favor, introduce un número de referencia válido.", "danger")
            return redirect(url_for("payment_form", order_id=order_id))
        
        # Check if reference number already exists in Payment to prevent duplicates
        existing_payment_ref = Payment.query.filter_by(reference_number=reference_number).first()
        if existing_payment_ref:
            flash("Este número de referencia ya ha sido utilizado. Por favor, verifica o contacta a soporte.", "warning")
            return redirect(url_for("payment_form", order_id=order_id))

        try:
            # Update order with payment reference
            order.payment_reference = reference_number
            order.status = 'payment_submitted' # Mark order as having payment submitted

            # Create a new Payment record
            new_payment = Payment(
                order_id=order.id,
                reference_number=reference_number,
                amount=order.total_amount,
                status='pending' # Payment is pending approval
            )
            db.session.add(new_payment)
            db.session.commit()

            flash("Número de referencia enviado exitosamente. Tu pago está pendiente de verificación.", "success")
            return redirect(url_for("invoice", order_id=order.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al registrar referencia de pago: {e}", exc_info=True)
            flash("Ocurrió un error al procesar tu referencia de pago. Inténtalo de nuevo.", "danger")
            return redirect(url_for("payment_form", order_id=order.id))

    return render_template(
        "payment_form.html",
        order=order,
        active_page="payment"
    )

@app.route("/invoice/<int:order_id>")
@login_required
def invoice(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not is_accountant():
        flash("No tienes permiso para ver esta factura.", "danger")
        return redirect(url_for("home"))
    
    payment_details = Payment.query.filter_by(order_id=order.id).first()
    
    return render_template(
        "invoice.html",
        order=order,
        items=order.items,
        payment_details=payment_details,
        active_page="invoice"
    )

@app.route("/my_invoices")
@login_required
def my_invoices():
    # Fetch all orders for the current user
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    
    # Optionally fetch payment details for each order to display status
    orders_with_details = []
    for order in user_orders:
        payment = Payment.query.filter_by(order_id=order.id).first()
        orders_with_details.append({
            "order": order,
            "payment_status": payment.status if payment else 'No Payment Info'
        })

    return render_template(
        "my_invoices.html",
        orders=orders_with_details,
        active_page="my_invoices"
    )


# ---- Rutas de Administrador (Accountant) ----
@app.route("/admin/payments")
@login_required
@accountant_required
def admin_payments():
    # Get all pending payments
    pending_payments = Payment.query.filter_by(status='pending').order_by(Payment.payment_date.asc()).all()
    
    # Get all approved/rejected payments for history
    processed_payments = Payment.query.filter(Payment.status.in_(['approved', 'rejected'])).order_by(Payment.approval_date.desc()).limit(20).all() # Show last 20

    return render_template(
        "payment_approval.html",
        pending_payments=pending_payments,
        processed_payments=processed_payments,
        active_page="admin_payments"
    )

@app.route("/admin/approve_payment/<int:payment_id>", methods=["POST"])
@login_required
@accountant_required
def approve_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    if payment.status == 'pending':
        try:
            payment.status = 'approved'
            payment.approved_by = current_user.id
            payment.approval_date = datetime.utcnow()
            
            # Update associated order status
            order = Order.query.get(payment.order_id)
            if order:
                order.status = 'approved'
                db.session.add(order)

            db.session.add(payment)
            db.session.commit()
            flash(f"Pago de referencia '{payment.reference_number}' aprobado para el pedido #{payment.order_id}.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al aprobar pago {payment_id}: {e}", exc_info=True)
            flash("Ocurrió un error al aprobar el pago. Inténtalo de nuevo.", "danger")
    else:
        flash("Este pago ya ha sido procesado.", "warning")
    
    return redirect(url_for("admin_payments"))

@app.route("/admin/reject_payment/<int:payment_id>", methods=["POST"])
@login_required
@accountant_required
def reject_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    if payment.status == 'pending':
        try:
            payment.status = 'rejected'
            payment.approved_by = current_user.id # Record who rejected it
            payment.approval_date = datetime.utcnow()
            
            # Optionally update associated order status
            order = Order.query.get(payment.order_id)
            if order:
                order.status = 'cancelled' # Or 'payment_rejected'
                flash(f"Pedido #{order.id} marcado como 'cancelado' debido a rechazo de pago.", "info")
                db.session.add(order)

            db.session.add(payment)
            db.session.commit()
            flash(f"Pago de referencia '{payment.reference_number}' rechazado para el pedido #{payment.order_id}.", "danger")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al rechazar pago {payment_id}: {e}", exc_info=True)
            flash("Ocurrió un error al rechazar el pago. Inténtalo de nuevo.", "danger")
    else:
        flash("Este pago ya ha sido procesado.", "warning")
    
    return redirect(url_for("admin_payments"))


@app.route("/compare")
@login_required
def compare():
    pharmacies = Pharmacy.query.all()
    product1_id = request.args.get("product1", type=int)
    product2_id = request.args.get("product2", type=int)

    # Obtener productos
    product1 = db.session.get(Product, product1_id) if product1_id else None
    product2 = db.session.get(Product, product2_id) if product2_id else None

    # Obtener IDs de farmacias de los productos si no se especifican
    pharmacy1_id = request.args.get("pharmacy1", type=int) or (
        product1.pharmacy_id if product1 else None
    )
    pharmacy2_id = request.args.get("pharmacy2", type=int) or (
        product2.pharmacy_id if product2 else None
    )

    # Obtener objetos de farmacia
    pharmacy1 = db.session.get(Pharmacy, pharmacy1_id) if pharmacy1_id else None
    pharmacy2 = db.session.get(Pharmacy, pharmacy2_id) if pharmacy2_id else None

    total_cart_items = get_total_cart_items()

    return render_template(
        "compare.html",
        product1=product1,
        product2=product2,
        pharmacy1=pharmacy1,
        pharmacy2=pharmacy2,
        pharmacy1_id=pharmacy1_id,
        pharmacy2_id=pharmacy2_id,
        active_page="compare",
        total_cart_items=total_cart_items,
    )


# ======================================================================
# RUTAS DE AUTENTICACIÓN CON PROTECCIÓN ADICIONAL
# ======================================================================


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("El usuario no existe. Por favor, regístrate primero.", "warning")
            return render_template(
                "login.html", title="Iniciar Sesión", form=form, hide_navbar_menu=True
            )
        if not check_password_hash(user.password, form.password.data):
            flash("Contraseña incorrecta. Intenta de nuevo.", "danger")
            return render_template(
                "login.html", title="Iniciar Sesión", form=form, hide_navbar_menu=True
            )
        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("home"))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en {getattr(form, field).label.text}: {error}", "danger")
    return render_template(
        "login.html", title="Iniciar Sesión", form=form, hide_navbar_menu=True
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash("El usuario o correo ya está registrado. Usa otros datos.", "warning")
            return render_template(
                "register.html", title="Registro", form=form, hide_navbar_menu=True
            )
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("¡Cuenta creada exitosamente! Ahora puedes iniciar sesión", "success")
        login_user(user)
        return redirect(url_for("home"))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error en {getattr(form, field).label.text}: {error}", "danger")
    return render_template(
        "register.html", title="Registro", form=form, hide_navbar_menu=True
    )


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    try:
        # Obtener el nombre de usuario antes de cerrar la sesión
        username = current_user.username

        # Cerrar la sesión con Flask-Login
        logout_user()

        # Limpiar la sesión
        session.clear()

        # Mensaje de éxito
        flash(
            f"Has cerrado sesión correctamente. ¡Hasta pronto, {username}!", "success"
        )

        # Redirigir al inicio
        return redirect(url_for("home"))

    except Exception as e:
        error_msg = f"Error al cerrar sesión: {str(e)}"
        current_app.logger.error(error_msg, exc_info=True)
        flash(
            "Ocurrió un error al cerrar sesión. Por favor, inténtalo de nuevo.", "error"
        )
        return redirect(url_for("home"))


# ======================================================================
# INICIO DE LA APLICACIÓN
# ======================================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
