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
            "name": "HealthPlus Pharmacy",
            "address": "123 Main Street, Anytown",
            "phone": "(555) 123-4567",
            "logo": "fa-solid fa-mortar-pestle",
            "color": "#009B77",
            "products": [
                {
                    "id": "p1_001",
                    "name": "Acetaminophen 500mg",
                    "category": "Pain Relief",
                    "description": "Pain reliever and fever reducer for mild to moderate pain",
                    "price": 8.99,
                    "unit": "100 tablets",
                    "in_stock": True,
                    "stock_quantity": 150
                },
                {
                    "id": "p1_002",
                    "name": "Ibuprofen 200mg",
                    "category": "Pain Relief",
                    "description": "Non-steroidal anti-inflammatory drug for pain relief",
                    "price": 7.49,
                    "unit": "50 tablets",
                    "in_stock": True,
                    "stock_quantity": 85
                },
                {
                    "id": "p1_003",
                    "name": "Loratadine 10mg",
                    "category": "Allergy",
                    "description": "24-hour non-drowsy allergy relief",
                    "price": 12.99,
                    "unit": "30 tablets",
                    "in_stock": True,
                    "stock_quantity": 42
                },
                {
                    "id": "p1_004",
                    "name": "Cetirizine HCl 10mg",
                    "category": "Allergy",
                    "description": "Relief from allergy symptoms for 24 hours",
                    "price": 15.49,
                    "unit": "30 tablets",
                    "in_stock": False,
                    "stock_quantity": 0
                },
                {
                    "id": "p1_005",
                    "name": "Multivitamin Adult",
                    "category": "Vitamins",
                    "description": "Complete daily multivitamin for adults",
                    "price": 19.99,
                    "unit": "90 tablets",
                    "in_stock": True,
                    "stock_quantity": 65
                },
                {
                    "id": "p1_006",
                    "name": "Vitamin D3 1000IU",
                    "category": "Vitamins",
                    "description": "Supports bone health and immune function",
                    "price": 11.29,
                    "unit": "100 softgels",
                    "in_stock": True,
                    "stock_quantity": 110
                },
                {
                    "id": "p1_007",
                    "name": "Omeprazole 20mg",
                    "category": "Digestive Health",
                    "description": "Treats frequent heartburn and acid reflux",
                    "price": 14.79,
                    "unit": "42 capsules",
                    "in_stock": True,
                    "stock_quantity": 38
                },
                {
                    "id": "p1_008",
                    "name": "Digital Thermometer",
                    "category": "Medical Devices",
                    "description": "Fast and accurate temperature readings",
                    "price": 12.99,
                    "unit": "1 device",
                    "in_stock": True,
                    "stock_quantity": 25
                },
                {
                    "id": "p1_009",
                    "name": "Blood Pressure Monitor",
                    "category": "Medical Devices",
                    "description": "Automatic blood pressure and pulse readings",
                    "price": 49.99,
                    "unit": "1 device",
                    "in_stock": False,
                    "stock_quantity": 0
                },
                {
                    "id": "p1_010",
                    "name": "First Aid Kit",
                    "category": "First Aid",
                    "description": "Complete kit for minor emergencies",
                    "price": 24.99,
                    "unit": "1 kit",
                    "in_stock": True,
                    "stock_quantity": 18
                }
            ]
        },
        "pharmacy2": {
            "name": "MediCare Pharmacy",
            "address": "456 Oak Avenue, Somewhere",
            "phone": "(555) 987-6543",
            "logo": "fa-solid fa-prescription-bottle-medical",
            "color": "#4A90E2",
            "products": [
                {
                    "id": "p2_001",
                    "name": "Acetaminophen 500mg",
                    "category": "Pain Relief",
                    "description": "Pain reliever and fever reducer for mild to moderate pain",
                    "price": 7.99,
                    "unit": "100 tablets",
                    "in_stock": True,
                    "stock_quantity": 120
                },
                {
                    "id": "p2_002",
                    "name": "Ibuprofen 200mg",
                    "category": "Pain Relief",
                    "description": "Non-steroidal anti-inflammatory drug for pain relief",
                    "price": 8.49,
                    "unit": "50 tablets",
                    "in_stock": True,
                    "stock_quantity": 65
                },
                {
                    "id": "p2_003",
                    "name": "Diphenhydramine 25mg",
                    "category": "Allergy",
                    "description": "Antihistamine for allergy relief and sleep aid",
                    "price": 6.99,
                    "unit": "24 tablets",
                    "in_stock": True,
                    "stock_quantity": 55
                },
                {
                    "id": "p2_004",
                    "name": "Cetirizine HCl 10mg",
                    "category": "Allergy",
                    "description": "Relief from allergy symptoms for 24 hours",
                    "price": 13.99,
                    "unit": "30 tablets",
                    "in_stock": True,
                    "stock_quantity": 28
                },
                {
                    "id": "p2_005",
                    "name": "Vitamin C 1000mg",
                    "category": "Vitamins",
                    "description": "Supports immune system health",
                    "price": 15.99,
                    "unit": "100 tablets",
                    "in_stock": True,
                    "stock_quantity": 90
                },
                {
                    "id": "p2_006",
                    "name": "Vitamin B Complex",
                    "category": "Vitamins",
                    "description": "Essential B vitamins for energy and metabolism",
                    "price": 17.49,
                    "unit": "60 tablets",
                    "in_stock": False,
                    "stock_quantity": 0
                },
                {
                    "id": "p2_007",
                    "name": "Famotidine 20mg",
                    "category": "Digestive Health",
                    "description": "Treats and prevents heartburn and acid indigestion",
                    "price": 9.99,
                    "unit": "50 tablets",
                    "in_stock": True,
                    "stock_quantity": 42
                },
                {
                    "id": "p2_008",
                    "name": "Digital Thermometer",
                    "category": "Medical Devices",
                    "description": "Fast and accurate temperature readings",
                    "price": 10.99,
                    "unit": "1 device",
                    "in_stock": True,
                    "stock_quantity": 15
                },
                {
                    "id": "p2_009",
                    "name": "Pulse Oximeter",
                    "category": "Medical Devices",
                    "description": "Measures blood oxygen level and pulse rate",
                    "price": 29.99,
                    "unit": "1 device",
                    "in_stock": True,
                    "stock_quantity": 12
                },
                {
                    "id": "p2_010",
                    "name": "Bandages Variety Pack",
                    "category": "First Aid",
                    "description": "Assorted sizes for minor wounds",
                    "price": 5.99,
                    "unit": "100 count",
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
