from app import app
from models import Pharmacy, Product
from sqlalchemy.exc import IntegrityError
from models import db
import os

# --- Datos de farmacias y productos ---
pharmacies_data = [
    {
        "name": "Farmatodo",
        "logo": "fa-solid fa-mortar-pestle",
        "color": "#009B77",
        "products": [
            {"code": "p1_001", "name": "Acetaminofén 500mg", "category": "Alivio del Dolor", "description": "Analgésico y antipirético para el dolor leve a moderado", "price": 8.99, "unit": "100 tabletas", "in_stock": True, "stock_quantity": 150},
            {"code": "p1_002", "name": "Ibuprofeno 200mg", "category": "Alivio del Dolor", "description": "Medicamento antiinflamatorio no esteroideo para el alivio del dolor", "price": 7.49, "unit": "50 tabletas", "in_stock": True, "stock_quantity": 85},
            {"code": "p1_003", "name": "Loratadina 10mg", "category": "Alergia", "description": "Alivio de alergias sin somnolencia durante 24 horas", "price": 12.99, "unit": "30 tabletas", "in_stock": True, "stock_quantity": 42},
            {"code": "p1_004", "name": "Cetirizina HCl 10mg", "category": "Alergia", "description": "Alivio de síntomas de alergia durante 24 horas", "price": 15.49, "unit": "30 tabletas", "in_stock": False, "stock_quantity": 0},
            {"code": "p1_005", "name": "Multivitamínico Adulto", "category": "Vitaminas", "description": "Multivitamínico diario completo para adultos", "price": 19.99, "unit": "90 tabletas", "in_stock": True, "stock_quantity": 65},
            {"code": "p1_006", "name": "Vitamina D3 1000UI", "category": "Vitaminas", "description": "Apoya la salud ósea y la función inmunológica", "price": 11.29, "unit": "100 cápsulas blandas", "in_stock": True, "stock_quantity": 110},
            {"code": "p1_007", "name": "Omeprazol 20mg", "category": "Salud Digestiva", "description": "Trata la acidez frecuente y el reflujo ácido", "price": 14.79, "unit": "42 cápsulas", "in_stock": True, "stock_quantity": 38},
            {"code": "p1_008", "name": "Termómetro Digital", "category": "Dispositivos Médicos", "description": "Lecturas de temperatura rápidas y precisas", "price": 12.99, "unit": "1 dispositivo", "in_stock": True, "stock_quantity": 25},
            {"code": "p1_009", "name": "Monitor de Presión Arterial", "category": "Dispositivos Médicos", "description": "Lecturas automáticas de presión arterial y pulso", "price": 49.99, "unit": "1 dispositivo", "in_stock": False, "stock_quantity": 0},
            {"code": "p1_010", "name": "Kit de Primeros Auxilios", "category": "Primeros Auxilios", "description": "Kit completo para emergencias menores", "price": 24.99, "unit": "1 kit", "in_stock": True, "stock_quantity": 18}
        ]
    },
    {
        "name": "Farmahorro",
        "logo": "fa-solid fa-prescription-bottle-medical",
        "color": "#4A90E2",
        "products": [
            {"code": "p2_001", "name": "Acetaminofén 500mg", "category": "Alivio del Dolor", "description": "Analgésico y antipirético para el dolor leve a moderado", "price": 7.99, "unit": "100 tabletas", "in_stock": True, "stock_quantity": 120},
            {"code": "p2_002", "name": "Ibuprofeno 200mg", "category": "Alivio del Dolor", "description": "Medicamento antiinflamatorio no esteroideo para el alivio del dolor", "price": 8.49, "unit": "50 tabletas", "in_stock": True, "stock_quantity": 65},
            {"code": "p2_003", "name": "Difenhidramina 25mg", "category": "Alergia", "description": "Antihistamínico para el alivio de alergias y ayuda para dormir", "price": 6.99, "unit": "24 tabletas", "in_stock": True, "stock_quantity": 55},
            {"code": "p2_004", "name": "Cetirizina HCl 10mg", "category": "Alergia", "description": "Alivio de síntomas de alergia durante 24 horas", "price": 13.99, "unit": "30 tabletas", "in_stock": True, "stock_quantity": 28},
            {"code": "p2_005", "name": "Vitamina C 1000mg", "category": "Vitaminas", "description": "Apoya la salud del sistema inmunológico", "price": 15.99, "unit": "100 tabletas", "in_stock": True, "stock_quantity": 90},
            {"code": "p2_006", "name": "Complejo B", "category": "Vitaminas", "description": "Vitaminas esenciales B para energía y metabolismo", "price": 17.49, "unit": "60 tabletas", "in_stock": False, "stock_quantity": 0},
            {"code": "p2_007", "name": "Famotidina 20mg", "category": "Salud Digestiva", "description": "Trata y previene la acidez estomacal y la indigestión ácida", "price": 9.99, "unit": "50 tabletas", "in_stock": True, "stock_quantity": 42},
            {"code": "p2_008", "name": "Termómetro Digital", "category": "Dispositivos Médicos", "description": "Lecturas de temperatura rápidas y precisas", "price": 10.99, "unit": "1 dispositivo", "in_stock": True, "stock_quantity": 15},
            {"code": "p2_009", "name": "Oxímetro de Pulso", "category": "Dispositivos Médicos", "description": "Mide el nivel de oxígeno en la sangre y la frecuencia del pulso", "price": 29.99, "unit": "1 dispositivo", "in_stock": True, "stock_quantity": 12},
            {"code": "p2_010", "name": "Paquete de Vendajes Variados", "category": "Primeros Auxilios", "description": "Tamaños surtidos para heridas menores", "price": 5.99, "unit": "100 unidades", "in_stock": True, "stock_quantity": 75}
        ]
    }
]

def populate():
    with app.app_context():
        db.drop_all()
        db.create_all()
        for pdata in pharmacies_data:
            # Evitar duplicados por nombre
            pharmacy = Pharmacy.query.filter_by(name=pdata["name"]).first()
            if not pharmacy:
                pharmacy = Pharmacy(name=pdata["name"], logo=pdata["logo"], color=pdata["color"])
                db.session.add(pharmacy)
                db.session.flush()  # Para obtener el id
            for prod in pdata["products"]:
                # Evitar duplicados por código
                product = Product.query.filter_by(code=prod["code"]).first()
                if not product:
                    product = Product(
                        code=prod["code"],
                        name=prod["name"],
                        category=prod["category"],
                        description=prod["description"],
                        price=prod["price"],
                        unit=prod["unit"],
                        in_stock=prod["in_stock"],
                        stock_quantity=prod["stock_quantity"],
                        pharmacy_id=pharmacy.id
                    )
                    db.session.add(product)
        try:
            db.session.commit()
            print("¡Base de datos poblada con farmacias y productos!")
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error de integridad: {e}")
        except Exception as e:
            db.session.rollback()
            print(f"Error inesperado: {e}")

# Ejecutar automáticamente al inicio si la base de datos no existe
if __name__ == "__main__" or not os.path.exists(os.path.join('instance', 'site.db')):
    populate()
