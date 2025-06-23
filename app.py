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
)
from forms import RegistrationForm, LoginForm
from models import db, Pharmacy, Product, User

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
app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET")

print(
    "Clave secreta configurada correctamente."
    if app.config["SECRET_KEY"]
    else "Error: No se pudo configurar la clave secreta."
)

# Configuración de cookies seguras para protección adicional
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Solo enviar cookies sobre HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevenir acceso a cookies via JavaScript
    SESSION_COOKIE_SAMESITE="Lax",  # Protección contra CSRF
    PERMANENT_SESSION_LIFETIME=3600,  # 1 hora de duración de la sesión
)

# Configurar la clave secreta para las sesiones
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
        "script-src": ["'self'", "https://cdn.jsdelivr.net", "'unsafe-inline'"],
        "font-src": ["'self'", "https://cdn.jsdelivr.net", "data:"],
        "img-src": [
            "'self'",
            "data:",
            "https://somoscomunidad.org.ve",
            "https://farmahorro.com.ve",
        ],
    },
    content_security_policy_nonce_in=["script-src"],
    frame_options="SAMEORIGIN",
    strict_transport_security=True,
    force_https=False,  # Solo si estás detrás de un proxy HTTPS
    session_cookie_http_only=True,  # CORRECCIÓN: http_only en lugar de httponly
    session_cookie_secure=True,
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


# Crear tablas en la base de datos SOLO si no existen
with app.app_context():
    db.create_all()

# ======================================================================
# FUNCIONALIDAD DE LA APLICACIÓN
# ======================================================================


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


# ======================================================================
# RUTAS DE LA APLICACIÓN
# ======================================================================


# Main route - displays both pharmacies
@app.route("/")
@login_required
def home():
    pharmacies = Pharmacy.query.all()
    total_cart_items = get_total_cart_items()
    return render_template(
        "index.html",
        pharmacies=pharmacies,
        active_page="home",
        total_cart_items=total_cart_items,
    )


@app.route("/pharmacy/<int:pharmacy_id>")
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
                f"Error: Producto con ID {product_id} no encontrado en la base de datos.",
                "error",
            )
    total_cart_items = get_total_cart_items()
    return render_template(
        "cart.html",
        cart_items=cart_items_details,
        total_price=total_price,
        total_cart_items=total_cart_items,
        active_page="cart",
    )


@app.route("/compare")
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