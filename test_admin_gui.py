#!/usr/bin/env python3
# Code created by https://linktr.ee/saran709
"""
Test Admin GUI Access
Quick script to test admin access in the GUI environment.
"""

import tkinter as tk
from tkinter import messagebox
from voting_system import VotingSystem
from admin_panel import AdminPanel

def test_admin_gui():
    """Test admin functionality in GUI"""
    print("Testing Admin GUI Access...")
    
    # Create a simple test window
    root = tk.Tk()
    root.title("Admin Test")
    root.geometry("400x300")
    
    # Initialize voting system
    voting_system = VotingSystem()
    
    # Create a simple GUI structure for testing
    class TestGUI:
        def __init__(self):
            self.current_frame = None
            self.root = root
        
        def clear_frame(self):
            if self.current_frame:
                self.current_frame.destroy()
    
    test_gui = TestGUI()
    
    # Create admin panel
    admin_panel = AdminPanel(test_gui, voting_system)
    
    def test_login():
        """Test admin login"""
        success, message = voting_system.login_admin("admin", "admin123")
        if success:
            messagebox.showinfo("Success", f"Admin login successful!\nAdmin status: {voting_system.is_admin}")
            admin_panel.setup_admin_screen()
        else:
            messagebox.showerror("Error", f"Login failed: {message}")
    
    # Create test button
    login_btn = tk.Button(
        root,
        text="Test Admin Login",
        command=test_login,
        bg='#3498db',
        fg='white',
        font=('Arial', 12),
        pady=10
    )
    login_btn.pack(pady=50)
    
    info_label = tk.Label(
        root,
        text="Click button to test admin login\nand access to admin panel",
        font=('Arial', 10),
        justify='center'
    )
    info_label.pack(pady=20)
    
    print("GUI test window opened. Click 'Test Admin Login' to test.")
    root.mainloop()

if __name__ == "__main__":
    test_admin_gui()