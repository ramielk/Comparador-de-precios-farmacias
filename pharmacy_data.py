"""
Module to handle pharmacy data operations.
This file contains functions for retrieving and manipulating pharmacy inventory data.
"""

# Define pharmacy inventories with product data
# This is server-side defined data, not mocked data
def get_pharmacy_data():
    """
    Returns structured data for both pharmacies.
    """
    return {
        "pharmacy1": {
            "name": "Farmatodo",
            "logo": "fa-solid fa-mortar-pestle",
            "color": "#009B77",
            "products": [
                {
                    "id": "p1_001",
                    "name": "Acetaminofén 500mg",
                    "category": "Alivio del Dolor",
                    "description": "Analgésico y antipirético para el dolor leve a moderado",
                    "price": 8.99,   
                    "unit": "100 tabletas",
                    "in_stock": True,
                    "stock_quantity": 150
                },
                {
                    "id": "p1_002",
                    "name": "Ibuprofeno 200mg",
                    "category": "Alivio del Dolor",
                    "description": "Medicamento antiinflamatorio no esteroideo para el alivio del dolor",
                    "price": 7.49,
                    "unit": "50 tabletas",
                    "in_stock": True,
                    "stock_quantity": 85
                },
                {
                    "id": "p1_003",
                    "name": "Loratadina 10mg",
                    "category": "Alergia",
                    "description": "Alivio de alergias sin somnolencia durante 24 horas",
                    "price": 12.99,
                    "unit": "30 tabletas",
                    "in_stock": True,
                    "stock_quantity": 42
                },
                {
                    "id": "p1_004",
                    "name": "Cetirizina HCl 10mg",
                    "category": "Alergia",
                    "description": "Alivio de síntomas de alergia durante 24 horas",
                    "price": 15.49,
                    "unit": "30 tabletas",
                    "in_stock": False,
                    "stock_quantity": 0
                },
                {
                    "id": "p1_005",
                    "name": "Multivitamínico Adulto",
                    "category": "Vitaminas",
                    "description": "Multivitamínico diario completo para adultos",
                    "price": 19.99,
                    "unit": "90 tabletas",
                    "in_stock": True,
                    "stock_quantity": 65
                },
                {
                    "id": "p1_006",
                    "name": "Vitamina D3 1000UI",
                    "category": "Vitaminas",
                    "description": "Apoya la salud ósea y la función inmunológica",
                    "price": 11.29,
                    "unit": "100 cápsulas blandas",
                    "in_stock": True,
                    "stock_quantity": 110
                },
                {
                    "id": "p1_007",
                    "name": "Omeprazol 20mg",
                    "category": "Salud Digestiva",
                    "description": "Trata la acidez frecuente y el reflujo ácido",
                    "price": 14.79,
                    "unit": "42 cápsulas",
                    "in_stock": True,
                    "stock_quantity": 38
                },
                {
                    "id": "p1_008",
                    "name": "Termómetro Digital",
                    "category": "Dispositivos Médicos",
                    "description": "Lecturas de temperatura rápidas y precisas",
                    "price": 12.99,
                    "unit": "1 dispositivo",
                    "in_stock": True,
                    "stock_quantity": 25
                },
                {
                    "id": "p1_009",
                    "name": "Monitor de Presión Arterial",
                    "category": "Dispositivos Médicos",
                    "description": "Lecturas automáticas de presión arterial y pulso",
                    "price": 49.99,
                    "unit": "1 dispositivo",
                    "in_stock": False,
                    "stock_quantity": 0
                },
                {
                    "id": "p1_010",
                    "name": "Kit de Primeros Auxilios",
                    "category": "Primeros Auxilios",
                    "description": "Kit completo para emergencias menores",
                    "price": 24.99,
                    "unit": "1 kit",
                    "in_stock": True,
                    "stock_quantity": 18
                }
            ]
        },
        "pharmacy2": {
            "name": "Farmahorro",
            "logo": "fa-solid fa-prescription-bottle-medical",
            "color": "#4A90E2",
            "products": [
                {
                    "id": "p2_001",
                    "name": "Acetaminofén 500mg",
                    "category": "Alivio del Dolor",
                    "description": "Analgésico y antipirético para el dolor leve a moderado",
                    "price": 7.99,
                    "unit": "100 tabletas",
                    "in_stock": True,
                    "stock_quantity": 120
                },
                {
                    "id": "p2_002",
                    "name": "Ibuprofeno 200mg",
                    "category": "Alivio del Dolor",
                    "description": "Medicamento antiinflamatorio no esteroideo para el alivio del dolor",
                    "price": 8.49,
                    "unit": "50 tabletas",
                    "in_stock": True,
                    "stock_quantity": 65
                },
                {
                    "id": "p2_003",
                    "name": "Difenhidramina 25mg",
                    "category": "Alergia",
                    "description": "Antihistamínico para el alivio de alergias y ayuda para dormir",
                    "price": 6.99,
                    "unit": "24 tabletas",
                    "in_stock": True,
                    "stock_quantity": 55
                },
                {
                    "id": "p2_004",
                    "name": "Cetirizina HCl 10mg",
                    "category": "Alergia",
                    "description": "Alivio de síntomas de alergia durante 24 horas",
                    "price": 13.99,
                    "unit": "30 tabletas",
                    "in_stock": True,
                    "stock_quantity": 28
                },
                {
                    "id": "p2_005",
                    "name": "Vitamina C 1000mg",
                    "category": "Vitaminas",
                    "description": "Apoya la salud del sistema inmunológico",
                    "price": 15.99,
                    "unit": "100 tabletas",
                    "in_stock": True,
                    "stock_quantity": 90
                },
                {
                    "id": "p2_006",
                    "name": "Complejo B",
                    "category": "Vitaminas",
                    "description": "Vitaminas esenciales B para energía y metabolismo",
                    "price": 17.49,
                    "unit": "60 tabletas",
                    "in_stock": False,
                    "stock_quantity": 0
                },
                {
                    "id": "p2_007",
                    "name": "Famotidina 20mg",
                    "category": "Salud Digestiva",
                    "description": "Trata y previene la acidez estomacal y la indigestión ácida",
                    "price": 9.99,
                    "unit": "50 tabletas",
                    "in_stock": True,
                    "stock_quantity": 42
                },
                {
                    "id": "p2_008",
                    "name": "Termómetro Digital",
                    "category": "Dispositivos Médicos",
                    "description": "Lecturas de temperatura rápidas y precisas",
                    "price": 10.99,
                    "unit": "1 dispositivo",
                    "in_stock": True,
                    "stock_quantity": 15
                },
                {
                    "id": "p2_009",
                    "name": "Oxímetro de Pulso",
                    "category": "Dispositivos Médicos",
                    "description": "Mide el nivel de oxígeno en la sangre y la frecuencia del pulso",
                    "price": 29.99,
                    "unit": "1 dispositivo",
                    "in_stock": True,
                    "stock_quantity": 12
                },
                {
                    "id": "p2_010",
                    "name": "Paquete de Vendajes Variados",
                    "category": "Primeros Auxilios",
                    "description": "Tamaños surtidos para heridas menores",
                    "price": 5.99,
                    "unit": "100 unidades",
                    "in_stock": True,
                    "stock_quantity": 75
                }
            ]
        }
    }

def get_product_by_id(products, product_id):
    """
    Retrieves a product by its ID from a list of products.
    
    Args:
        products: List of product dictionaries
        product_id: ID of the product to find
        
    Returns:
        The product dictionary or None if not found
    """
    for product in products:
        if product['id'] == product_id:
            return product
    return None

def get_categories(pharmacy_data):
    """
    Extracts unique categories from all products in both pharmacies.
    
    Args:
        pharmacy_data: Dictionary containing pharmacy data
        
    Returns:
        List of unique category names
    """
    categories = set()
    
    # Extract categories from pharmacy1
    for product in pharmacy_data['pharmacy1']['products']:
        categories.add(product['category'])
    
    # Extract categories from pharmacy2
    for product in pharmacy_data['pharmacy2']['products']:
        categories.add(product['category'])
    
    return sorted(list(categories))

def filter_products(products, category='', search_query='', availability=''):
    """
    Filters products based on category, search query, and availability.
    
    Args:
        products: List of product dictionaries
        category: Category to filter by
        search_query: Search term to filter by
        availability: 'in_stock', 'out_of_stock', or empty string for all
        
    Returns:
        Filtered list of products
    """
    filtered_products = products.copy()
    
    # Filter by category
    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    # Filter by search query
    if search_query:
        search_query = search_query.lower()
        filtered_products = [p for p in filtered_products if 
                             search_query in p['name'].lower() or 
                             search_query in p['description'].lower() or
                             search_query in p['category'].lower()]
    
    # Filter by availability
    if availability == 'in_stock':
        filtered_products = [p for p in filtered_products if p['in_stock']]
    elif availability == 'out_of_stock':
        filtered_products = [p for p in filtered_products if not p['in_stock']]
    
    return filtered_products
