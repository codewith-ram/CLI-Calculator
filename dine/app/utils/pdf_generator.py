"""
PDF generation utilities for SmartDine Desktop Edition
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import Dict, Any, List
import os


class PDFGenerator:
    """Generate PDF documents for bills and reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        ))
        
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.darkblue
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        ))
    
    def generate_bill_pdf(self, bill_data: Dict[str, Any], output_path: str) -> bool:
        """Generate a PDF bill"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # Restaurant header
            story.append(Paragraph("SmartDine Restaurant", self.styles['CustomTitle']))
            story.append(Paragraph("123 Main Street, City, State 12345", self.styles['CustomSubtitle']))
            story.append(Paragraph("Phone: (555) 123-4567", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 20))
            
            # Bill information
            story.append(Paragraph(f"Bill #: {bill_data['id']}", self.styles['CustomHeader']))
            story.append(Paragraph(f"Table: {bill_data['table_number']}", self.styles['CustomNormal']))
            story.append(Paragraph(f"Cashier: {bill_data['cashier_name']}", self.styles['CustomNormal']))
            story.append(Paragraph(f"Date: {bill_data['created_at'].strftime('%Y-%m-%d %H:%M:%S')}", self.styles['CustomNormal']))
            story.append(Spacer(1, 20))
            
            # Order items table
            story.append(Paragraph("Order Details", self.styles['CustomHeader']))
            
            # Prepare table data
            table_data = [['Item', 'Qty', 'Price', 'Total']]
            for item in bill_data['order_items']:
                table_data.append([
                    item['menu_item_name'],
                    str(item['quantity']),
                    f"${item['unit_price']:.2f}",
                    f"${item['total_price']:.2f}"
                ])
            
            # Create table
            table = Table(table_data, colWidths=[3*inch, 0.8*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
            
            # Bill summary
            story.append(Paragraph("Bill Summary", self.styles['CustomHeader']))
            
            summary_data = [
                ['Subtotal:', f"${bill_data['subtotal']:.2f}"],
                ['Tax:', f"${bill_data['tax_amount']:.2f}"],
                ['Service Charge:', f"${bill_data['service_charge']:.2f}"],
                ['Discount:', f"-${bill_data['discount_amount']:.2f}"],
                ['TOTAL:', f"${bill_data['total_amount']:.2f}"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1*inch])
            summary_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 14),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.darkred)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Payment information
            story.append(Paragraph(f"Payment Method: {bill_data['payment_method'].upper()}", self.styles['CustomNormal']))
            story.append(Paragraph(f"Status: {bill_data['payment_status'].upper()}", self.styles['CustomNormal']))
            story.append(Spacer(1, 30))
            
            # Footer
            story.append(Paragraph("Thank you for dining with us!", self.styles['CustomSubtitle']))
            story.append(Paragraph("Please come again!", self.styles['CustomNormal']))
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def generate_sales_report_pdf(self, report_data: Dict[str, Any], output_path: str) -> bool:
        """Generate a PDF sales report"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # Report header
            story.append(Paragraph("SmartDine Sales Report", self.styles['CustomTitle']))
            story.append(Paragraph(f"Period: {report_data['start_date']} to {report_data['end_date']}", self.styles['CustomSubtitle']))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['CustomNormal']))
            story.append(Spacer(1, 20))
            
            # Sales summary
            story.append(Paragraph("Sales Summary", self.styles['CustomHeader']))
            
            summary_data = [
                ['Total Revenue:', f"${report_data['total_revenue']:.2f}"],
                ['Total Bills:', str(report_data['total_bills'])],
                ['Total Tax:', f"${report_data['total_tax']:.2f}"],
                ['Total Discount:', f"${report_data['total_discount']:.2f}"],
                ['Average Bill:', f"${report_data['average_bill']:.2f}"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Top menu items
            if 'top_menu_items' in report_data:
                story.append(Paragraph("Top Menu Items", self.styles['CustomHeader']))
                
                menu_data = [['Item', 'Quantity', 'Revenue']]
                for item in report_data['top_menu_items'][:10]:  # Top 10 items
                    menu_data.append([
                        item['name'],
                        str(item['total_quantity']),
                        f"${item['total_revenue']:.2f}"
                    ])
                
                menu_table = Table(menu_data, colWidths=[2.5*inch, 1*inch, 1*inch])
                menu_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(menu_table)
                story.append(Spacer(1, 20))
            
            # Footer
            story.append(Paragraph("End of Report", self.styles['CustomNormal']))
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating PDF report: {e}")
            return False
    
    def generate_daily_summary_pdf(self, summary_data: Dict[str, Any], output_path: str) -> bool:
        """Generate a PDF daily summary"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # Header
            story.append(Paragraph("SmartDine Daily Summary", self.styles['CustomTitle']))
            story.append(Paragraph(f"Date: {summary_data['date']}", self.styles['CustomSubtitle']))
            story.append(Spacer(1, 20))
            
            # Summary data
            story.append(Paragraph("Daily Statistics", self.styles['CustomHeader']))
            
            stats_data = [
                ['Total Bills:', str(summary_data['total_bills'])],
                ['Total Revenue:', f"${summary_data['total_revenue']:.2f}"],
                ['Total Tax:', f"${summary_data['total_tax']:.2f}"],
                ['Total Discount:', f"${summary_data['total_discount']:.2f}"],
                ['Average Bill:', f"${summary_data['average_bill_amount']:.2f}"]
            ]
            
            stats_table = Table(stats_data, colWidths=[2*inch, 1.5*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Payment methods breakdown
            if 'payment_methods' in summary_data:
                story.append(Paragraph("Payment Methods", self.styles['CustomHeader']))
                
                payment_data = [['Method', 'Count']]
                for method, count in summary_data['payment_methods'].items():
                    payment_data.append([method.upper(), str(count)])
                
                payment_table = Table(payment_data, colWidths=[2*inch, 1*inch])
                payment_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(payment_table)
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating daily summary PDF: {e}")
            return False


# Global PDF generator instance
pdf_generator = PDFGenerator()
