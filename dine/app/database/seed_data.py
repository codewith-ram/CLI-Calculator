"""
Seed data for SmartDine Desktop Edition
"""
from sqlalchemy.orm import Session
from .models import User, MenuItem, Table
from .db_connection import get_db_session
from backend.auth_service import auth_service


def create_sample_users():
    """Create sample users for testing"""
    users_data = [
        {
            'username': 'admin',
            'password': 'admin123',
            'role': 'admin',
            'full_name': 'System Administrator',
            'email': 'admin@smartdine.com'
        },
        {
            'username': 'waiter1',
            'password': 'waiter123',
            'role': 'waiter',
            'full_name': 'John Smith',
            'email': 'john@smartdine.com'
        },
        {
            'username': 'waiter2',
            'password': 'waiter123',
            'role': 'waiter',
            'full_name': 'Sarah Johnson',
            'email': 'sarah@smartdine.com'
        },
        {
            'username': 'chef1',
            'password': 'chef123',
            'role': 'chef',
            'full_name': 'Michael Brown',
            'email': 'michael@smartdine.com'
        },
        {
            'username': 'cashier1',
            'password': 'cashier123',
            'role': 'cashier',
            'full_name': 'Emily Davis',
            'email': 'emily@smartdine.com'
        }
    ]
    
    for user_data in users_data:
        auth_service.create_user(**user_data)


def create_sample_menu_items():
    """Create sample menu items"""
    session = get_db_session()
    try:
        menu_items_data = [
            # Starters
            {
                'name': 'Caesar Salad',
                'description': 'Fresh romaine lettuce with caesar dressing, croutons, and parmesan cheese',
                'price': 8.99,
                'category': 'starters',
                'is_available': True
            },
            {
                'name': 'Buffalo Wings',
                'description': 'Spicy chicken wings served with ranch dressing',
                'price': 12.99,
                'category': 'starters',
                'is_available': True
            },
            {
                'name': 'Mozzarella Sticks',
                'description': 'Crispy breaded mozzarella sticks with marinara sauce',
                'price': 7.99,
                'category': 'starters',
                'is_available': True
            },
            {
                'name': 'Soup of the Day',
                'description': 'Chef\'s special soup served with bread',
                'price': 6.99,
                'category': 'starters',
                'is_available': True
            },
            
            # Main Course
            {
                'name': 'Grilled Salmon',
                'description': 'Fresh Atlantic salmon grilled to perfection with lemon butter sauce',
                'price': 24.99,
                'category': 'main_course',
                'is_available': True
            },
            {
                'name': 'Ribeye Steak',
                'description': '12oz ribeye steak cooked to your preference with garlic mashed potatoes',
                'price': 32.99,
                'category': 'main_course',
                'is_available': True
            },
            {
                'name': 'Chicken Parmesan',
                'description': 'Breaded chicken breast with marinara sauce and mozzarella cheese',
                'price': 18.99,
                'category': 'main_course',
                'is_available': True
            },
            {
                'name': 'Pasta Carbonara',
                'description': 'Creamy pasta with bacon, eggs, and parmesan cheese',
                'price': 16.99,
                'category': 'main_course',
                'is_available': True
            },
            {
                'name': 'Vegetarian Burger',
                'description': 'House-made veggie patty with lettuce, tomato, and special sauce',
                'price': 14.99,
                'category': 'main_course',
                'is_available': True
            },
            
            # Desserts
            {
                'name': 'Chocolate Cake',
                'description': 'Rich chocolate layer cake with chocolate ganache',
                'price': 7.99,
                'category': 'desserts',
                'is_available': True
            },
            {
                'name': 'Tiramisu',
                'description': 'Classic Italian dessert with coffee and mascarpone',
                'price': 8.99,
                'category': 'desserts',
                'is_available': True
            },
            {
                'name': 'Ice Cream Sundae',
                'description': 'Vanilla ice cream with chocolate sauce, whipped cream, and cherry',
                'price': 5.99,
                'category': 'desserts',
                'is_available': True
            },
            {
                'name': 'Cheesecake',
                'description': 'New York style cheesecake with berry compote',
                'price': 6.99,
                'category': 'desserts',
                'is_available': True
            },
            
            # Beverages
            {
                'name': 'Coffee',
                'description': 'Freshly brewed coffee',
                'price': 2.99,
                'category': 'beverages',
                'is_available': True
            },
            {
                'name': 'Tea',
                'description': 'Selection of premium teas',
                'price': 2.49,
                'category': 'beverages',
                'is_available': True
            },
            {
                'name': 'Soft Drinks',
                'description': 'Coca-Cola, Pepsi, Sprite, or 7-Up',
                'price': 2.99,
                'category': 'beverages',
                'is_available': True
            },
            {
                'name': 'Fresh Juice',
                'description': 'Orange, Apple, or Cranberry juice',
                'price': 3.99,
                'category': 'beverages',
                'is_available': True
            },
            {
                'name': 'Bottled Water',
                'description': 'Premium bottled water',
                'price': 1.99,
                'category': 'beverages',
                'is_available': True
            }
        ]
        
        for item_data in menu_items_data:
            menu_item = MenuItem(**item_data)
            session.add(menu_item)
        
        session.commit()
    finally:
        session.close()


def create_sample_tables():
    """Create sample tables"""
    session = get_db_session()
    try:
        tables_data = [
            {'table_number': 1, 'capacity': 2, 'status': 'free'},
            {'table_number': 2, 'capacity': 4, 'status': 'free'},
            {'table_number': 3, 'capacity': 2, 'status': 'free'},
            {'table_number': 4, 'capacity': 6, 'status': 'free'},
            {'table_number': 5, 'capacity': 4, 'status': 'free'},
            {'table_number': 6, 'capacity': 8, 'status': 'free'},
            {'table_number': 7, 'capacity': 2, 'status': 'free'},
            {'table_number': 8, 'capacity': 4, 'status': 'free'},
            {'table_number': 9, 'capacity': 6, 'status': 'free'},
            {'table_number': 10, 'capacity': 10, 'status': 'free'},
            {'table_number': 11, 'capacity': 2, 'status': 'free'},
            {'table_number': 12, 'capacity': 4, 'status': 'free'},
            {'table_number': 13, 'capacity': 6, 'status': 'free'},
            {'table_number': 14, 'capacity': 8, 'status': 'free'},
            {'table_number': 15, 'capacity': 4, 'status': 'free'}
        ]
        
        for table_data in tables_data:
            table = Table(**table_data)
            session.add(table)
        
        session.commit()
    finally:
        session.close()


def seed_database():
    """Seed the database with sample data"""
    print("Seeding database with sample data...")
    
    # Create sample users
    print("Creating sample users...")
    create_sample_users()
    
    # Create sample menu items
    print("Creating sample menu items...")
    create_sample_menu_items()
    
    # Create sample tables
    print("Creating sample tables...")
    create_sample_tables()
    
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    from db_connection import init_database
    init_database()
    seed_database()
