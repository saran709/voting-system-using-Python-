# Code created by https://linktr.ee/saran709
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from voting_system import VotingSystem
from admin_panel import AdminPanel

class VotingGUI:
    """
    Main GUI interface for the voting system
    """
    
    def __init__(self):
        self.voting_system = VotingSystem()
        self.root = tk.Tk()
        self.root.title("Offline Voting System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.current_frame = None
        
        # Initialize admin panel
        self.admin_panel = AdminPanel(self, self.voting_system)
        
        # Initialize the interface
        self.setup_login_screen()
        
    def clear_frame(self):
        """Clear the current frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def setup_login_screen(self):
        """Setup the login screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            self.current_frame, 
            text="Offline Voting System", 
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Login Type Selection
        login_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        login_frame.pack(pady=20)
        
        # Voter Login Section
        voter_frame = tk.LabelFrame(
            login_frame, 
            text="Voter Login", 
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        voter_frame.pack(side='left', padx=20, pady=10, fill='both', expand=True)
        
        tk.Label(voter_frame, text="Voter ID:", bg='#f0f0f0').pack(pady=5)
        self.voter_id_entry = tk.Entry(voter_frame, font=('Arial', 11))
        self.voter_id_entry.pack(pady=5, padx=10, fill='x')
        
        tk.Label(voter_frame, text="Password:", bg='#f0f0f0').pack(pady=5)
        self.voter_password_entry = tk.Entry(voter_frame, show="*", font=('Arial', 11))
        self.voter_password_entry.pack(pady=5, padx=10, fill='x')
        
        voter_login_btn = tk.Button(
            voter_frame, 
            text="Login as Voter", 
            command=self.voter_login,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            pady=10
        )
        voter_login_btn.pack(pady=10, padx=10, fill='x')
        
        # Admin Login Section
        admin_frame = tk.LabelFrame(
            login_frame, 
            text="Admin Login", 
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        admin_frame.pack(side='right', padx=20, pady=10, fill='both', expand=True)
        
        tk.Label(admin_frame, text="Admin ID:", bg='#f0f0f0').pack(pady=5)
        self.admin_id_entry = tk.Entry(admin_frame, font=('Arial', 11))
        self.admin_id_entry.pack(pady=5, padx=10, fill='x')
        
        tk.Label(admin_frame, text="Password:", bg='#f0f0f0').pack(pady=5)
        self.admin_password_entry = tk.Entry(admin_frame, show="*", font=('Arial', 11))
        self.admin_password_entry.pack(pady=5, padx=10, fill='x')
        
        admin_login_btn = tk.Button(
            admin_frame, 
            text="Login as Admin", 
            command=self.admin_login,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 11, 'bold'),
            pady=10
        )
        admin_login_btn.pack(pady=10, padx=10, fill='x')
        
        # Information Section
        info_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        info_frame.pack(pady=20, fill='x')
        
        info_text = tk.Text(
            info_frame, 
            height=8, 
            bg='#ecf0f1', 
            fg='#2c3e50',
            font=('Arial', 10),
            wrap='word',
            state='disabled'
        )
        info_text.pack(fill='x', padx=20)
        
        info_content = """
Welcome to the Offline Voting System!

INSTRUCTIONS:
• Voters: Login with your registered voter ID and password to cast your vote
• Admins: Login with your admin credentials to manage the system
• Each voter can only vote once
• All data is stored securely in a local SQLite database

FEATURES:
• Secure offline voting system
• Real-time results and statistics
• Anonymous vote storage
• Duplicate voting prevention

Contact your system administrator for login credentials if needed.
        """
        
        info_text.config(state='normal')
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.voter_login())
    
    def voter_login(self):
        """Handle voter login"""
        voter_id = self.voter_id_entry.get().strip()
        password = self.voter_password_entry.get()
        
        if not voter_id or not password:
            messagebox.showerror("Error", "Please enter both Voter ID and Password")
            return
        
        success, message, voter_name = self.voting_system.login_voter(voter_id, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.setup_voting_screen(voter_name)
        else:
            messagebox.showerror("Login Failed", message)
    
    def admin_login(self):
        """Handle admin login"""
        admin_id = self.admin_id_entry.get().strip()
        password = self.admin_password_entry.get()
        
        if not admin_id or not password:
            messagebox.showerror("Error", "Please enter both Admin ID and Password")
            return
        
        success, message = self.voting_system.login_admin(admin_id, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.admin_panel.setup_admin_screen()
        else:
            messagebox.showerror("Login Failed", message)
    
    def setup_voting_screen(self, voter_name):
        """Setup the voting screen for voters"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 20))
        
        welcome_label = tk.Label(
            header_frame, 
            text=f"Welcome, {voter_name}!", 
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        welcome_label.pack(side='left')
        
        logout_btn = tk.Button(
            header_frame, 
            text="Logout", 
            command=self.logout,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10)
        )
        logout_btn.pack(side='right')
        
        # Instructions
        instruction_label = tk.Label(
            self.current_frame, 
            text="Please select your preferred candidate and click 'Cast Vote'", 
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#34495e'
        )
        instruction_label.pack(pady=10)
        
        # Candidates Frame
        candidates_frame = tk.LabelFrame(
            self.current_frame, 
            text="Candidates", 
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0'
        )
        candidates_frame.pack(fill='both', expand=True, pady=10)
        
        # Get candidates
        candidates = self.voting_system.get_candidates()
        
        if not candidates:
            no_candidates_label = tk.Label(
                candidates_frame, 
                text="No candidates available. Please contact the administrator.", 
                font=('Arial', 12),
                bg='#f0f0f0',
                fg='#e74c3c'
            )
            no_candidates_label.pack(pady=20)
            return
        
        # Candidate selection
        self.selected_candidate = tk.IntVar()
        
        for candidate_id, name, party, description in candidates:
            candidate_frame = tk.Frame(candidates_frame, bg='white', relief='raised', bd=1)
            candidate_frame.pack(fill='x', padx=10, pady=5)
            
            # Radio button
            radio_btn = tk.Radiobutton(
                candidate_frame,
                variable=self.selected_candidate,
                value=candidate_id,
                bg='white',
                font=('Arial', 11)
            )
            radio_btn.pack(side='left', padx=10, pady=10)
            
            # Candidate info
            info_frame = tk.Frame(candidate_frame, bg='white')
            info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            
            name_label = tk.Label(
                info_frame, 
                text=name, 
                font=('Arial', 12, 'bold'),
                bg='white',
                fg='#2c3e50'
            )
            name_label.pack(anchor='w')
            
            if party:
                party_label = tk.Label(
                    info_frame, 
                    text=f"Party: {party}", 
                    font=('Arial', 10),
                    bg='white',
                    fg='#7f8c8d'
                )
                party_label.pack(anchor='w')
            
            if description:
                desc_label = tk.Label(
                    info_frame, 
                    text=description, 
                    font=('Arial', 9),
                    bg='white',
                    fg='#95a5a6',
                    wraplength=400
                )
                desc_label.pack(anchor='w')
        
        # Vote button
        vote_btn = tk.Button(
            self.current_frame, 
            text="Cast Vote", 
            command=self.cast_vote,
            bg='#27ae60',
            fg='white',
            font=('Arial', 14, 'bold'),
            pady=15
        )
        vote_btn.pack(pady=20, padx=50, fill='x')
    
    def cast_vote(self):
        """Handle vote casting"""
        if not hasattr(self, 'selected_candidate') or not self.selected_candidate.get():
            messagebox.showerror("Error", "Please select a candidate before casting your vote")
            return
        
        # Confirm vote
        candidate_id = self.selected_candidate.get()
        candidates = self.voting_system.get_candidates()
        candidate_info = next((c for c in candidates if c[0] == candidate_id), None)
        
        if not candidate_info:
            messagebox.showerror("Error", "Invalid candidate selection")
            return
        
        candidate_name = candidate_info[1]
        candidate_party = candidate_info[2]
        
        confirm_message = f"Are you sure you want to vote for:\n\n"
        confirm_message += f"Candidate: {candidate_name}\n"
        if candidate_party:
            confirm_message += f"Party: {candidate_party}\n"
        confirm_message += f"\nThis action cannot be undone."
        
        confirm = messagebox.askyesno(
            "Confirm Vote", 
            confirm_message,
            icon='question'
        )
        
        if not confirm:
            return
        
        # Cast the vote
        success, message = self.voting_system.cast_vote(candidate_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.show_vote_confirmation(candidate_name, candidate_party)
        else:
            messagebox.showerror("Error", message)
    
    def show_vote_confirmation(self, candidate_name, candidate_party=None):
        """Show vote confirmation screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Success message
        success_label = tk.Label(
            self.current_frame, 
            text="✓ Vote Cast Successfully!", 
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#27ae60'
        )
        success_label.pack(pady=50)
        
        # Vote details
        details_frame = tk.Frame(self.current_frame, bg='#ecf0f1', relief='raised', bd=2)
        details_frame.pack(pady=20, padx=50, fill='x')
        
        tk.Label(
            details_frame,
            text="Vote Details:",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=(15, 5))
        
        tk.Label(
            details_frame,
            text=f"Candidate: {candidate_name}",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#2c3e50'
        ).pack(pady=2)
        
        if candidate_party:
            tk.Label(
                details_frame,
                text=f"Party: {candidate_party}",
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#2c3e50'
            ).pack(pady=2)
        
        # Get current timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tk.Label(
            details_frame,
            text=f"Time: {timestamp}",
            font=('Arial', 10),
            bg='#ecf0f1',
            fg='#7f8c8d'
        ).pack(pady=(2, 15))
        
        thanks_label = tk.Label(
            self.current_frame, 
            text="Thank you for participating in the election!\nYour vote has been recorded and will be reflected in the results.", 
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#7f8c8d',
            justify='center'
        )
        thanks_label.pack(pady=20)
        
        # Return to login button
        return_btn = tk.Button(
            self.current_frame, 
            text="Return to Login", 
            command=self.logout,
            bg='#3498db',
            fg='white',
            font=('Arial', 12),
            pady=10
        )
        return_btn.pack(pady=30)
    
    def logout(self):
        """Logout and return to login screen"""
        self.voting_system.logout()
        self.setup_login_screen()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()