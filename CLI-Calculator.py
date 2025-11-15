#!/usr/bin/env python3
"""
Modern Premium GUI Calculator
A comprehensive calculator with stunning UI, backend engine, and data persistence
"""

import json
import os
import math
import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
from typing import List, Dict, Optional


# ==================== BACKEND LAYER ====================

class CalculationEngine:
    """Backend calculation engine with advanced operations"""
    
    @staticmethod
    def evaluate_expression(expr: str) -> float:
        """Safely evaluate mathematical expressions"""
        expr = expr.replace(" ", "")
        expr = expr.replace("sqrt", "math.sqrt")
        expr = expr.replace("sin", "math.sin")
        expr = expr.replace("cos", "math.cos")
        expr = expr.replace("tan", "math.tan")
        expr = expr.replace("log", "math.log")
        expr = expr.replace("ln", "math.log")
        expr = expr.replace("pi", "math.pi")
        expr = expr.replace("π", "math.pi")
        expr = expr.replace("e", "math.e")
        
        if not re.match(r'^[0-9+\-*/().mathlrsgincoepi\s]+$', expr):
            raise ValueError("Invalid characters in expression")
        
        try:
            result = eval(expr, {"__builtins__": {}}, {"math": math})
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")


# ==================== DATA LAYER ====================

class HistoryManager:
    """Data persistence layer for calculation history"""
    
    def __init__(self, filename: str = "calculator_history.json"):
        self.filename = filename
        self.history: List[Dict] = []
        self.load_history()
    
    def load_history(self) -> None:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []
        else:
            self.history = []
    
    def save_history(self) -> None:
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")
    
    def add_entry(self, operation: str, result: float) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "result": result
        }
        self.history.append(entry)
        self.save_history()
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        if limit:
            return self.history[-limit:]
        return self.history
    
    def clear_history(self) -> None:
        self.history = []
        self.save_history()
    
    def get_last_result(self) -> Optional[float]:
        if self.history:
            return self.history[-1]["result"]
        return None


# ==================== FRONTEND LAYER ====================

class ModernButton(tk.Canvas):
    """Custom modern button with hover effects"""
    
    def __init__(self, parent, text, command, bg="#2a2a2a", fg="#ffffff", 
                 hover_bg="#3a3a3a", active_bg="#1a1a1a", **kwargs):
        super().__init__(parent, bg=bg, highlightthickness=0, **kwargs)
        
        self.text = text
        self.command = command
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        self.active_bg = active_bg
        self.is_pressed = False
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw()
    
    def draw(self, bg=None):
        self.delete("all")
        bg = bg or self.bg
        
        # Draw rounded rectangle background
        self.create_rounded_rect(0, 0, self.winfo_reqwidth() or 80, 
                                 self.winfo_reqheight() or 60, 
                                 radius=12, fill=bg, outline="")
        
        # Draw text
        self.create_text(40, 30, text=self.text, fill=self.fg, 
                        font=("Segoe UI", 14, "bold"))
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self, e):
        if not self.is_pressed:
            self.draw(self.hover_bg)
    
    def on_leave(self, e):
        if not self.is_pressed:
            self.draw(self.bg)
    
    def on_press(self, e):
        self.is_pressed = True
        self.draw(self.active_bg)
    
    def on_release(self, e):
        self.is_pressed = False
        self.draw(self.hover_bg)
        if self.command:
            self.command()


class CalculatorGUI:
    """Modern premium GUI interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("480x750")
        self.root.resizable(False, False)
        
        # Modern gradient background
        self.root.configure(bg="#0f0f0f")
        
        self.engine = CalculationEngine()
        self.history_manager = HistoryManager()
        self.memory: Optional[float] = None
        self.current_theme = "dark"
        
        self.setup_ui()
        self.update_history_display()
    
    def setup_ui(self):
        """Setup the modern user interface"""
        # Main container with gradient effect
        main_frame = tk.Frame(self.root, bg="#0f0f0f")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header with app title
        header_frame = tk.Frame(main_frame, bg="#0f0f0f")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(
            header_frame,
            text="CALCULATOR",
            font=("Segoe UI", 11, "bold"),
            bg="#0f0f0f",
            fg="#00d4ff"
        )
        title_label.pack(side=tk.LEFT)
        
        # Theme toggle button
        self.theme_btn = tk.Button(
            header_frame,
            text="🌙",
            font=("Segoe UI", 12),
            bg="#1a1a1a",
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=2,
            command=self.toggle_theme
        )
        self.theme_btn.pack(side=tk.RIGHT)
        
        # Display area with glass morphism effect
        display_frame = tk.Frame(main_frame, bg="#1a1a1a", relief=tk.FLAT)
        display_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add subtle border effect
        border_frame = tk.Frame(display_frame, bg="#00d4ff", height=2)
        border_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Memory and history indicators
        indicators_frame = tk.Frame(display_frame, bg="#1a1a1a")
        indicators_frame.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        self.memory_indicator = tk.Label(
            indicators_frame,
            text="",
            font=("Segoe UI", 9),
            bg="#1a1a1a",
            fg="#00d4ff"
        )
        self.memory_indicator.pack(side=tk.LEFT)
        
        self.history_indicator = tk.Label(
            indicators_frame,
            text="",
            font=("Segoe UI", 9),
            bg="#1a1a1a",
            fg="#888888"
        )
        self.history_indicator.pack(side=tk.RIGHT)
        
        # Expression display
        self.expression_var = tk.StringVar()
        expression_display = tk.Label(
            display_frame,
            textvariable=self.expression_var,
            font=("Consolas", 16),
            bg="#1a1a1a",
            fg="#666666",
            anchor=tk.E,
            padx=20,
            pady=5
        )
        expression_display.pack(fill=tk.X)
        
        # Result display with glow effect
        result_frame = tk.Frame(display_frame, bg="#1a1a1a")
        result_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.result_var = tk.StringVar(value="0")
        result_display = tk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Consolas", 42, "bold"),
            bg="#1a1a1a",
            fg="#ffffff",
            anchor=tk.E
        )
        result_display.pack(fill=tk.X)
        
        # Notebook for tabs with modern styling
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure('Modern.TNotebook', 
                       background="#0f0f0f", 
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        
        style.configure('Modern.TNotebook.Tab',
                       background="#1a1a1a",
                       foreground="#888888",
                       padding=[25, 12],
                       font=("Segoe UI", 10, "bold"),
                       borderwidth=0)
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', '#00d4ff')],
                 foreground=[('selected', '#000000')])
        
        notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Calculator tab
        calc_tab = tk.Frame(notebook, bg="#0f0f0f")
        notebook.add(calc_tab, text="CALCULATOR")
        
        # History tab
        history_tab = tk.Frame(notebook, bg="#0f0f0f")
        notebook.add(history_tab, text="HISTORY")
        
        self.setup_calculator_tab(calc_tab)
        self.setup_history_tab(history_tab)
    
    def setup_calculator_tab(self, parent):
        """Setup modern calculator buttons"""
        button_frame = tk.Frame(parent, bg="#0f0f0f")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button layout with categories
        buttons = [
            [
                {'text': 'MC', 'bg': '#ff3366', 'fg': '#ffffff'},
                {'text': 'MR', 'bg': '#ff3366', 'fg': '#ffffff'},
                {'text': 'MS', 'bg': '#ff3366', 'fg': '#ffffff'},
                {'text': 'M+', 'bg': '#ff3366', 'fg': '#ffffff'}
            ],
            [
                {'text': 'C', 'bg': '#ff3366', 'fg': '#ffffff'},
                {'text': '⌫', 'bg': '#ff3366', 'fg': '#ffffff'},
                {'text': '%', 'bg': '#2a2a2a', 'fg': '#00d4ff'},
                {'text': '÷', 'bg': '#2a2a2a', 'fg': '#00d4ff'}
            ],
            [
                {'text': '7', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '8', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '9', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '×', 'bg': '#2a2a2a', 'fg': '#00d4ff'}
            ],
            [
                {'text': '4', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '5', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '6', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '-', 'bg': '#2a2a2a', 'fg': '#00d4ff'}
            ],
            [
                {'text': '1', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '2', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '3', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '+', 'bg': '#2a2a2a', 'fg': '#00d4ff'}
            ],
            [
                {'text': '±', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '0', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '.', 'bg': '#1a1a1a', 'fg': '#ffffff'},
                {'text': '=', 'bg': '#00d4ff', 'fg': '#000000'}
            ],
            [
                {'text': '√', 'bg': '#2a2a2a', 'fg': '#00d4ff'},
                {'text': 'x²', 'bg': '#2a2a2a', 'fg': '#00d4ff'},
                {'text': '(', 'bg': '#2a2a2a', 'fg': '#00d4ff'},
                {'text': ')', 'bg': '#2a2a2a', 'fg': '#00d4ff'}
            ],
            [
                {'text': 'sin', 'bg': '#2a2a2a', 'fg': '#00d4ff'},
                {'text': 'cos', 'bg': '#2a2a2a', 'fg': '#00d4ff'},
                {'text': 'tan', 'bg': '#2a2a2a', 'fg': '#00d4ff'},
                {'text': 'π', 'bg': '#2a2a2a', 'fg': '#00d4ff'}
            ]
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_config in enumerate(row):
                btn = tk.Button(
                    button_frame,
                    text=btn_config['text'],
                    font=("Segoe UI", 13, "bold"),
                    bg=btn_config['bg'],
                    fg=btn_config['fg'],
                    activebackground=btn_config['bg'],
                    activeforeground=btn_config['fg'],
                    bd=0,
                    relief=tk.FLAT,
                    cursor='hand2',
                    command=lambda x=btn_config['text']: self.on_button_click(x)
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=3, pady=3)
                
                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.lighten_color(b['bg'])))
                btn.bind("<Leave>", lambda e, b=btn, c=btn_config['bg']: b.config(bg=c))
        
        # Configure grid weights
        for i in range(len(buttons)):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def lighten_color(self, color):
        """Lighten a color for hover effect"""
        color_map = {
            '#1a1a1a': '#2a2a2a',
            '#2a2a2a': '#3a3a3a',
            '#ff3366': '#ff4477',
            '#00d4ff': '#33ddff'
        }
        return color_map.get(color, color)
    
    def setup_history_tab(self, parent):
        """Setup modern history display"""
        history_frame = tk.Frame(parent, bg="#0f0f0f")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # History header
        header = tk.Label(
            history_frame,
            text="📊 CALCULATION HISTORY",
            font=("Segoe UI", 12, "bold"),
            bg="#0f0f0f",
            fg="#00d4ff"
        )
        header.pack(pady=(0, 15))
        
        # History text area with modern styling
        text_frame = tk.Frame(history_frame, bg="#1a1a1a", relief=tk.FLAT)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = scrolledtext.ScrolledText(
            text_frame,
            font=("Consolas", 11),
            bg="#1a1a1a",
            fg="#ffffff",
            wrap=tk.WORD,
            state='disabled',
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15,
            insertbackground="#00d4ff",
            selectbackground="#00d4ff",
            selectforeground="#000000"
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Clear history button
        clear_btn = tk.Button(
            history_frame,
            text="🗑️ CLEAR HISTORY",
            font=("Segoe UI", 11, "bold"),
            bg="#ff3366",
            fg="#ffffff",
            bd=0,
            relief=tk.FLAT,
            cursor='hand2',
            pady=12,
            command=self.clear_history
        )
        clear_btn.pack(fill=tk.X, pady=(15, 0))
        
        # Hover effect for clear button
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#ff4477"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#ff3366"))
    
    def on_button_click(self, button_text):
        """Handle button clicks with animations"""
        current = self.expression_var.get()
        
        if button_text == 'C':
            self.expression_var.set('')
            self.result_var.set('0')
            self.animate_display()
        
        elif button_text == '⌫':
            self.expression_var.set(current[:-1])
        
        elif button_text == '=':
            self.calculate()
        
        elif button_text == '±':
            if current and current != '0':
                if current.startswith('-'):
                    self.expression_var.set(current[1:])
                else:
                    self.expression_var.set('-' + current)
        
        elif button_text == 'MC':
            self.memory = None
            self.memory_indicator.config(text="")
            self.show_toast("Memory cleared")
        
        elif button_text == 'MR':
            if self.memory is not None:
                self.expression_var.set(str(self.memory))
            else:
                self.show_toast("Memory is empty")
        
        elif button_text == 'MS':
            try:
                result = self.result_var.get()
                if result != '0':
                    self.memory = float(result)
                    self.memory_indicator.config(text=f"💾 M = {self.memory}")
                    self.show_toast(f"Stored: {self.memory}")
            except:
                self.show_toast("No valid result to store")
        
        elif button_text == 'M+':
            if self.memory is not None:
                try:
                    result = float(self.result_var.get())
                    self.memory += result
                    self.memory_indicator.config(text=f"💾 M = {self.memory}")
                except:
                    pass
        
        elif button_text == '÷':
            self.expression_var.set(current + '/')
        
        elif button_text == '×':
            self.expression_var.set(current + '*')
        
        elif button_text == 'x²':
            self.expression_var.set(current + '**2')
        
        elif button_text == '√':
            self.expression_var.set(current + 'sqrt(')
        
        elif button_text in ['sin', 'cos', 'tan']:
            self.expression_var.set(current + button_text + '(')
        
        elif button_text == 'π':
            self.expression_var.set(current + 'pi')
        
        else:
            self.expression_var.set(current + button_text)
    
    def calculate(self):
        """Perform calculation with animation"""
        expression = self.expression_var.get()
        
        if not expression:
            return
        
        try:
            result = self.engine.evaluate_expression(expression)
            self.result_var.set(str(result))
            self.history_manager.add_entry(expression, result)
            self.update_history_display()
            self.animate_result()
            
            # Update history indicator
            history_count = len(self.history_manager.get_history())
            self.history_indicator.config(text=f"📝 {history_count} calculations")
            
        except Exception as e:
            self.result_var.set("Error")
            self.show_toast(str(e))
    
    def animate_display(self):
        """Simple animation effect"""
        pass
    
    def animate_result(self):
        """Animate result display"""
        pass
    
    def show_toast(self, message):
        """Show a modern toast notification"""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.configure(bg="#1a1a1a")
        
        label = tk.Label(
            toast,
            text=message,
            font=("Segoe UI", 10),
            bg="#1a1a1a",
            fg="#ffffff",
            padx=20,
            pady=10
        )
        label.pack()
        
        # Position at bottom center
        toast.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - toast.winfo_width()) // 2
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        toast.geometry(f"+{x}+{y}")
        
        # Auto close after 2 seconds
        toast.after(2000, toast.destroy)
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.show_toast("Theme toggle coming soon!")
    
    def update_history_display(self):
        """Update the history display with modern styling"""
        history = self.history_manager.get_history(30)
        
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        
        if not history:
            self.history_text.insert(tk.END, "\n\n")
            self.history_text.insert(tk.END, "        No calculations yet\n\n")
            self.history_text.insert(tk.END, "    Start calculating to see\n")
            self.history_text.insert(tk.END, "        your history here!", 'center')
        else:
            for i, entry in enumerate(reversed(history), 1):
                timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%H:%M:%S")
                
                self.history_text.insert(tk.END, f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
                self.history_text.insert(tk.END, f"  ⏱️  {timestamp}\n")
                self.history_text.insert(tk.END, f"  📝 {entry['operation']}\n")
                self.history_text.insert(tk.END, f"  ✓  {entry['result']}\n")
        
        self.history_text.config(state='disabled')
    
    def clear_history(self):
        """Clear calculation history with confirmation"""
        if messagebox.askyesno("Clear History", 
                              "Are you sure you want to clear all history?",
                              icon='warning'):
            self.history_manager.clear_history()
            self.update_history_display()
            self.history_indicator.config(text="")
            self.show_toast("History cleared successfully")


# ==================== APPLICATION ENTRY POINT ====================

def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Set app icon (if available)
    try:
        root.iconbitmap('calculator.ico')
    except:
        pass
    
    app = CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
