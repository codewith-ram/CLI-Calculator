"""
Chart generation utilities for SmartDine Desktop Edition
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, date
from typing import List, Dict, Any
import os


class ChartGenerator:
    """Generate charts and graphs for analytics"""
    
    def __init__(self):
        plt.style.use('default')
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def create_sales_chart(self, daily_data: List[Dict[str, Any]], output_path: str = None) -> Figure:
        """Create a sales revenue chart"""
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        dates = [item['date'] for item in daily_data]
        revenues = [item['revenue'] for item in daily_data]
        
        ax.plot(dates, revenues, marker='o', linewidth=2, markersize=6, color=self.colors[0])
        ax.set_title('Daily Sales Revenue', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Revenue ($)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        fig.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_top_items_chart(self, items_data: List[Dict[str, Any]], output_path: str = None) -> Figure:
        """Create a bar chart of top menu items"""
        fig = Figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        names = [item['name'][:20] + '...' if len(item['name']) > 20 else item['name'] 
                for item in items_data]
        quantities = [item['total_quantity'] for item in items_data]
        
        bars = ax.bar(range(len(names)), quantities, color=self.colors[:len(names)])
        ax.set_title('Top Menu Items by Quantity Sold', fontsize=16, fontweight='bold')
        ax.set_xlabel('Menu Items', fontsize=12)
        ax.set_ylabel('Quantity Sold', fontsize=12)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        
        # Add value labels on bars
        for i, (bar, quantity) in enumerate(zip(bars, quantities)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   str(quantity), ha='center', va='bottom')
        
        fig.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_category_sales_pie(self, category_data: List[Dict[str, Any]], output_path: str = None) -> Figure:
        """Create a pie chart of sales by category"""
        fig = Figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        
        categories = [item['category'].replace('_', ' ').title() for item in category_data]
        revenues = [item['total_revenue'] for item in category_data]
        
        wedges, texts, autotexts = ax.pie(revenues, labels=categories, autopct='%1.1f%%',
                                        colors=self.colors[:len(categories)],
                                        startangle=90)
        
        ax.set_title('Sales by Category', fontsize=16, fontweight='bold')
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        fig.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_hourly_sales_chart(self, hourly_data: List[Dict[str, Any]], output_path: str = None) -> Figure:
        """Create a bar chart of hourly sales pattern"""
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        
        hours = [item['hour'] for item in hourly_data]
        revenues = [item['revenue'] for item in hourly_data]
        
        bars = ax.bar(hours, revenues, color=self.colors[0], alpha=0.7)
        ax.set_title('Hourly Sales Pattern', fontsize=16, fontweight='bold')
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Revenue ($)', fontsize=12)
        ax.set_xticks(hours)
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, revenue in zip(bars, revenues):
            if revenue > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       f'${revenue:.0f}', ha='center', va='bottom', fontsize=8)
        
        fig.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_waiter_performance_chart(self, waiter_data: List[Dict[str, Any]], output_path: str = None) -> Figure:
        """Create a bar chart of waiter performance"""
        fig = Figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        
        names = [waiter['waiter_name'] for waiter in waiter_data]
        revenues = [waiter['total_revenue'] for waiter in waiter_data]
        
        bars = ax.bar(range(len(names)), revenues, color=self.colors[:len(names)])
        ax.set_title('Waiter Performance by Revenue', fontsize=16, fontweight='bold')
        ax.set_xlabel('Waiters', fontsize=12)
        ax.set_ylabel('Total Revenue ($)', fontsize=12)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        
        # Add value labels on bars
        for i, (bar, revenue) in enumerate(zip(bars, revenues)):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   f'${revenue:.0f}', ha='center', va='bottom')
        
        fig.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_table_occupancy_chart(self, table_data: List[Dict[str, Any]], output_path: str = None) -> Figure:
        """Create a chart showing table occupancy rates"""
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        table_numbers = [table['table_number'] for table in table_data]
        order_counts = [table['order_count'] for table in table_data]
        
        bars = ax.bar(table_numbers, order_counts, color=self.colors[0], alpha=0.7)
        ax.set_title('Table Usage by Order Count', fontsize=16, fontweight='bold')
        ax.set_xlabel('Table Number', fontsize=12)
        ax.set_ylabel('Number of Orders', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, count in zip(bars, order_counts):
            if count > 0:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       str(count), ha='center', va='bottom')
        
        fig.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_dashboard_summary(self, summary_data: Dict[str, Any], output_path: str = None) -> Figure:
        """Create a dashboard summary with multiple metrics"""
        fig = Figure(figsize=(15, 10))
        
        # Create subplots
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        
        # 1. Revenue trend (if available)
        if 'daily_revenue' in summary_data:
            daily_data = summary_data['daily_revenue']
            dates = [item['date'] for item in daily_data]
            revenues = [item['revenue'] for item in daily_data]
            ax1.plot(dates, revenues, marker='o', color=self.colors[0])
            ax1.set_title('Daily Revenue Trend')
            ax1.set_ylabel('Revenue ($)')
            ax1.grid(True, alpha=0.3)
        
        # 2. Top items
        if 'top_items' in summary_data:
            items_data = summary_data['top_items'][:5]  # Top 5
            names = [item['name'][:15] + '...' if len(item['name']) > 15 else item['name'] 
                    for item in items_data]
            quantities = [item['total_quantity'] for item in items_data]
            ax2.bar(names, quantities, color=self.colors[1])
            ax2.set_title('Top 5 Menu Items')
            ax2.set_ylabel('Quantity Sold')
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. Category breakdown
        if 'category_sales' in summary_data:
            cat_data = summary_data['category_sales']
            categories = [cat['category'].replace('_', ' ').title() for cat in cat_data]
            revenues = [cat['total_revenue'] for cat in cat_data]
            ax3.pie(revenues, labels=categories, autopct='%1.1f%%', 
                   colors=self.colors[:len(categories)])
            ax3.set_title('Sales by Category')
        
        # 4. Payment methods
        if 'payment_methods' in summary_data:
            methods = list(summary_data['payment_methods'].keys())
            counts = list(summary_data['payment_methods'].values())
            ax4.bar(methods, counts, color=self.colors[2])
            ax4.set_title('Payment Methods')
            ax4.set_ylabel('Number of Transactions')
        
        fig.suptitle('SmartDine Analytics Dashboard', fontsize=16, fontweight='bold')
        fig.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
        
        return fig


# Global chart generator instance
chart_generator = ChartGenerator()
