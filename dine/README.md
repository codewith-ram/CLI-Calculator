# SmartDine Desktop Edition

A comprehensive Python full-stack GUI restaurant management system for desktop use.

## Features

- **Multi-role User System**: Admin, Waiter, Chef, and Cashier roles with different permissions
- **Menu Management**: Add, edit, delete menu items with categories and pricing
- **Table Management**: Manage restaurant tables with real-time status tracking
- **Order Processing**: Complete order workflow from waiter to kitchen to completion
- **Billing & Payments**: Generate bills, process payments, and print invoices
- **Analytics & Reports**: Sales reports, top items, revenue analysis
- **Offline Operation**: SQLite database for local data storage
- **Modern GUI**: Built with PyQt5 for a professional desktop experience

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd smartdine_desktop
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app/main.py
   ```

## Default Login Credentials

The application comes with sample data including default users:

- **Admin**: username: `admin`, password: `admin123`
- **Waiter**: username: `waiter1`, password: `waiter123`
- **Chef**: username: `chef1`, password: `chef123`
- **Cashier**: username: `cashier1`, password: `cashier123`

## User Roles

### Admin
- Manage menu items and categories
- Manage tables and capacity
- User management (add/edit users)
- Generate reports and analytics
- System administration

### Waiter
- View available tables
- Take customer orders
- Add menu items to orders
- View order history

### Chef
- View pending orders
- Update order status (cooking → ready → served)
- Kitchen workflow management

### Cashier
- Process bills for completed orders
- Handle payments (cash, card, UPI)
- Print invoices
- Payment processing

## Project Structure

```
smartdine_desktop/
├── app/
│   ├── main.py                     # Application entry point
│   ├── config.py                   # Configuration settings
│   ├── gui/                        # GUI components
│   │   ├── main_window.py          # Main application window
│   │   ├── login_window.py         # Login interface
│   │   ├── waiter_window.py        # Waiter interface
│   │   ├── chef_window.py          # Chef interface
│   │   ├── cashier_window.py       # Cashier interface
│   │   ├── admin_window.py         # Admin interface
│   │   └── dialogs/                # Dialog windows
│   ├── backend/                    # Business logic
│   │   ├── auth_service.py         # Authentication
│   │   ├── menu_service.py         # Menu management
│   │   ├── order_service.py        # Order processing
│   │   ├── billing_service.py      # Billing & payments
│   │   ├── table_service.py        # Table management
│   │   └── report_service.py       # Analytics & reports
│   ├── database/                   # Database layer
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── db_connection.py        # Database connection
│   │   └── seed_data.py            # Sample data
│   └── utils/                      # Utilities
│       ├── logger.py               # Logging
│       ├── validators.py           # Input validation
│       ├── pdf_generator.py        # PDF generation
│       └── chart_generator.py      # Chart generation
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Technology Stack

- **Frontend**: PyQt5 for modern desktop GUI
- **Backend**: Python with SQLAlchemy ORM
- **Database**: SQLite for local storage
- **Reports**: ReportLab for PDF generation
- **Charts**: Matplotlib for analytics
- **Security**: bcrypt for password hashing

## Key Features

### Order Workflow
1. **Waiter** takes order at table
2. **Order** appears in **Chef** kitchen view
3. **Chef** updates status: Pending → Cooking → Ready
4. **Waiter** serves completed order
5. **Cashier** processes payment and generates bill

### Real-time Updates
- Table status updates automatically
- Order status synchronized across roles
- Live data refresh every 5-30 seconds

### Reporting & Analytics
- Daily sales summaries
- Top-selling menu items
- Revenue by date range
- Table occupancy statistics
- Payment method breakdowns

## Configuration

Edit `app/config.py` to customize:
- Theme colors
- Database settings
- Business rules (tax rates, etc.)
- UI preferences

## Database

The application uses SQLite for local storage. The database file (`smartdine.db`) is created automatically on first run with sample data.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Errors**: Delete `smartdine.db` to reset the database

3. **GUI Issues**: Ensure PyQt5 is properly installed
   ```bash
   pip install PyQt5==5.15.9
   ```

## Development

### Adding New Features
1. Create new service in `app/backend/`
2. Add GUI components in `app/gui/`
3. Update database models if needed
4. Add tests in `app/tests/`

### Database Schema
- Users: Authentication and roles
- MenuItems: Restaurant menu
- Tables: Table management
- Orders: Customer orders
- OrderItems: Individual order items
- Bills: Billing and payments

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please check the documentation or create an issue in the repository.
