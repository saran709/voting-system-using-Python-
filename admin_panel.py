# Code created by https://linktr.ee/saran709
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from voting_system import VotingSystem

class AdminPanel:
    """
    Admin panel interface for managing the voting system
    """
    
    def __init__(self, parent_gui, voting_system):
        self.parent_gui = parent_gui
        self.voting_system = voting_system
        self.root = parent_gui.root
        self.current_frame = None
    
    def setup_admin_screen(self):
        """Setup the admin dashboard"""
        # Clear the parent GUI frame first
        self.parent_gui.clear_frame()
        
        # Set the current frame in parent GUI
        self.current_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.parent_gui.current_frame = self.current_frame
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, 
            text="Admin Dashboard", 
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(side='left')
        
        # Admin status indicator
        admin_status_label = tk.Label(
            header_frame,
            text=f"Admin: {'Logged In' if self.voting_system.is_admin else 'Not Logged In'}",
            font=('Arial', 10),
            bg='#27ae60' if self.voting_system.is_admin else '#e74c3c',
            fg='white',
            padx=10,
            pady=2
        )
        admin_status_label.pack(side='left', padx=(20, 0))
        
        logout_btn = tk.Button(
            header_frame, 
            text="Logout", 
            command=self.logout,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10)
        )
        logout_btn.pack(side='right')
        
        # Statistics Section
        self.create_statistics_section()
        
        # Tab Control
        self.notebook = ttk.Notebook(self.current_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)
        
        # Create tabs
        self.create_candidates_tab()
        self.create_voters_tab()
        self.create_results_tab()
        self.create_settings_tab()
    
    def clear_frame(self):
        """Clear the current frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def create_statistics_section(self):
        """Create the statistics overview section"""
        stats_frame = tk.LabelFrame(
            self.current_frame, 
            text="System Overview", 
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0'
        )
        stats_frame.pack(fill='x', pady=10)
        
        # Get statistics
        stats = self.voting_system.get_statistics()
        
        # Create statistics grid
        stats_grid = tk.Frame(stats_frame, bg='#f0f0f0')
        stats_grid.pack(fill='x', padx=10, pady=10)
        
        # Statistics cards
        self.create_stat_card(stats_grid, "Total Voters", stats['total_voters'], 0, 0, '#3498db')
        self.create_stat_card(stats_grid, "Total Candidates", stats['total_candidates'], 0, 1, '#e74c3c')
        self.create_stat_card(stats_grid, "Votes Cast", stats['total_votes'], 0, 2, '#27ae60')
        self.create_stat_card(stats_grid, "Turnout", f"{stats['voter_turnout']:.1f}%", 0, 3, '#f39c12')
    
    def create_stat_card(self, parent, title, value, row, col, color):
        """Create a statistics card"""
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        value_label = tk.Label(
            card_frame, 
            text=str(value), 
            font=('Arial', 16, 'bold'),
            bg=color,
            fg='white'
        )
        value_label.pack(pady=(10, 5))
        
        title_label = tk.Label(
            card_frame, 
            text=title, 
            font=('Arial', 10),
            bg=color,
            fg='white'
        )
        title_label.pack(pady=(0, 10))
    
    def create_candidates_tab(self):
        """Create the candidates management tab"""
        candidates_frame = ttk.Frame(self.notebook)
        self.notebook.add(candidates_frame, text="Manage Candidates")
        
        # Add candidate section
        add_frame = tk.LabelFrame(candidates_frame, text="Add New Candidate", font=('Arial', 12, 'bold'))
        add_frame.pack(fill='x', padx=10, pady=10)
        
        # Input fields
        fields_frame = tk.Frame(add_frame)
        fields_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(fields_frame, text="Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.candidate_name_entry = tk.Entry(fields_frame, font=('Arial', 11))
        self.candidate_name_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        tk.Label(fields_frame, text="Party:").grid(row=1, column=0, sticky='w', pady=5)
        self.candidate_party_entry = tk.Entry(fields_frame, font=('Arial', 11))
        self.candidate_party_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        tk.Label(fields_frame, text="Description:").grid(row=2, column=0, sticky='w', pady=5)
        self.candidate_desc_entry = tk.Entry(fields_frame, font=('Arial', 11))
        self.candidate_desc_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        add_btn = tk.Button(
            add_frame, 
            text="Add Candidate", 
            command=self.add_candidate,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11)
        )
        add_btn.pack(pady=10)
        
        # Candidates list
        list_frame = tk.LabelFrame(candidates_frame, text="Current Candidates", font=('Arial', 12, 'bold'))
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for candidates
        columns = ('ID', 'Name', 'Party', 'Description')
        self.candidates_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.candidates_tree.heading(col, text=col)
            self.candidates_tree.column(col, width=100)
        
        # Scrollbar
        candidates_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.candidates_tree.yview)
        self.candidates_tree.configure(yscrollcommand=candidates_scrollbar.set)
        
        self.candidates_tree.pack(side='left', fill='both', expand=True)
        candidates_scrollbar.pack(side='right', fill='y')
        
        # Remove button
        remove_candidate_btn = tk.Button(
            list_frame, 
            text="Remove Selected", 
            command=self.remove_candidate,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10)
        )
        remove_candidate_btn.pack(pady=5)
        
        self.refresh_candidates_list()
    
    def create_voters_tab(self):
        """Create the voters management tab"""
        voters_frame = ttk.Frame(self.notebook)
        self.notebook.add(voters_frame, text="Manage Voters")
        
        # Register voter section
        register_frame = tk.LabelFrame(voters_frame, text="Register New Voter", font=('Arial', 12, 'bold'))
        register_frame.pack(fill='x', padx=10, pady=10)
        
        # Input fields
        voter_fields_frame = tk.Frame(register_frame)
        voter_fields_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(voter_fields_frame, text="Voter ID:").grid(row=0, column=0, sticky='w', pady=5)
        self.voter_id_entry = tk.Entry(voter_fields_frame, font=('Arial', 11))
        self.voter_id_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        tk.Label(voter_fields_frame, text="Name:").grid(row=1, column=0, sticky='w', pady=5)
        self.voter_name_entry = tk.Entry(voter_fields_frame, font=('Arial', 11))
        self.voter_name_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        tk.Label(voter_fields_frame, text="Password:").grid(row=2, column=0, sticky='w', pady=5)
        self.voter_password_entry = tk.Entry(voter_fields_frame, show="*", font=('Arial', 11))
        self.voter_password_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        voter_fields_frame.grid_columnconfigure(1, weight=1)
        
        register_btn = tk.Button(
            register_frame, 
            text="Register Voter", 
            command=self.register_voter,
            bg='#3498db',
            fg='white',
            font=('Arial', 11)
        )
        register_btn.pack(pady=10)
        
        # Voters list
        voters_list_frame = tk.LabelFrame(voters_frame, text="Registered Voters", font=('Arial', 12, 'bold'))
        voters_list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for voters
        voter_columns = ('Voter ID', 'Name', 'Has Voted', 'Registration Date')
        self.voters_tree = ttk.Treeview(voters_list_frame, columns=voter_columns, show='headings')
        
        for col in voter_columns:
            self.voters_tree.heading(col, text=col)
            self.voters_tree.column(col, width=120)
        
        # Scrollbar
        voters_scrollbar = ttk.Scrollbar(voters_list_frame, orient='vertical', command=self.voters_tree.yview)
        self.voters_tree.configure(yscrollcommand=voters_scrollbar.set)
        
        self.voters_tree.pack(side='left', fill='both', expand=True)
        voters_scrollbar.pack(side='right', fill='y')
        
        self.refresh_voters_list()
    
    def create_results_tab(self):
        """Create the results viewing tab"""
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text="View Results")
        
        # Results display
        results_display_frame = tk.LabelFrame(results_frame, text="Voting Results", font=('Arial', 12, 'bold'))
        results_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Results treeview
        result_columns = ('Rank', 'Candidate', 'Party', 'Votes', 'Percentage')
        self.results_tree = ttk.Treeview(results_display_frame, columns=result_columns, show='headings')
        
        for col in result_columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120)
        
        # Scrollbar
        results_scrollbar = ttk.Scrollbar(results_display_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        results_scrollbar.pack(side='right', fill='y')
        
        # Buttons
        buttons_frame = tk.Frame(results_display_frame)
        buttons_frame.pack(fill='x', pady=10)
        
        refresh_btn = tk.Button(
            buttons_frame, 
            text="Refresh Results", 
            command=self.refresh_results,
            bg='#3498db',
            fg='white',
            font=('Arial', 10)
        )
        refresh_btn.pack(side='left', padx=5)
        
        export_btn = tk.Button(
            buttons_frame, 
            text="Export Summary", 
            command=self.export_results,
            bg='#f39c12',
            fg='white',
            font=('Arial', 10)
        )
        export_btn.pack(side='left', padx=5)
        
        # Auto-refresh toggle
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_check = tk.Checkbutton(
            buttons_frame,
            text="Auto-refresh (5s)",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh,
            bg='#f0f0f0'
        )
        auto_refresh_check.pack(side='left', padx=10)
        
        # Recent activity section
        activity_frame = tk.LabelFrame(results_frame, text="Recent Voting Activity", font=('Arial', 12, 'bold'))
        activity_frame.pack(fill='x', padx=10, pady=10)
        
        # Recent votes treeview
        activity_columns = ('Time', 'Candidate', 'Party')
        self.activity_tree = ttk.Treeview(activity_frame, columns=activity_columns, show='headings', height=6)
        
        for col in activity_columns:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, width=150)
        
        self.activity_tree.pack(fill='x', padx=10, pady=10)
        
        self.refresh_results()
        self.refresh_recent_activity()
        
        # Start auto-refresh
        self.start_auto_refresh()
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Database info
        db_info_frame = tk.LabelFrame(settings_frame, text="Database Information", font=('Arial', 12, 'bold'))
        db_info_frame.pack(fill='x', padx=10, pady=10)
        
        db_info_text = scrolledtext.ScrolledText(db_info_frame, height=10, state='disabled')
        db_info_text.pack(fill='x', padx=10, pady=10)
        
        # Display database info
        stats = self.voting_system.get_statistics()
        info_content = f"""
Database Status: Connected
Database File: voting_database.db
Total Tables: 4 (voters, candidates, votes, admin)

Current Statistics:
• Total Voters: {stats['total_voters']}
• Total Candidates: {stats['total_candidates']}
• Total Votes: {stats['total_votes']}
• Voter Turnout: {stats['voter_turnout']:.1f}%

Default Admin Credentials:
• Username: admin
• Password: [Contact system administrator]

System Information:
• Offline Mode: Enabled
• Database Type: SQLite
• Security: Password Hashing (SHA-256)
• Vote Privacy: Anonymous voting
        """
        
        db_info_text.config(state='normal')
        db_info_text.insert('1.0', info_content)
        db_info_text.config(state='disabled')
    
    def add_candidate(self):
        """Add a new candidate"""
        name = self.candidate_name_entry.get().strip()
        party = self.candidate_party_entry.get().strip()
        description = self.candidate_desc_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Candidate name is required")
            return
        
        # Check admin status
        if not self.voting_system.is_admin:
            messagebox.showerror("Error", "Admin access required. Please login as admin first.")
            return
        
        success, message = self.voting_system.add_candidate(name, party, description)
        
        if success:
            messagebox.showinfo("Success", message)
            self.candidate_name_entry.delete(0, tk.END)
            self.candidate_party_entry.delete(0, tk.END)
            self.candidate_desc_entry.delete(0, tk.END)
            self.refresh_candidates_list()
            self.refresh_statistics()
        else:
            messagebox.showerror("Error", message)
    
    def remove_candidate(self):
        """Remove selected candidate"""
        selection = self.candidates_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a candidate to remove")
            return
        
        item = self.candidates_tree.item(selection[0])
        candidate_id = item['values'][0]
        candidate_name = item['values'][1]
        
        confirm = messagebox.askyesno(
            "Confirm", 
            f"Are you sure you want to remove {candidate_name}?\n\nThis will also remove all votes for this candidate.",
            icon='warning'
        )
        
        if confirm:
            success, message = self.voting_system.remove_candidate(candidate_id)
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_candidates_list()
                self.refresh_statistics()
            else:
                messagebox.showerror("Error", message)
    
    def register_voter(self):
        """Register a new voter"""
        voter_id = self.voter_id_entry.get().strip()
        name = self.voter_name_entry.get().strip()
        password = self.voter_password_entry.get()
        
        if not voter_id or not name or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        # Check admin status
        if not self.voting_system.is_admin:
            messagebox.showerror("Error", "Admin access required. Please login as admin first.")
            return
        
        success, message = self.voting_system.register_voter(voter_id, name, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.voter_id_entry.delete(0, tk.END)
            self.voter_name_entry.delete(0, tk.END)
            self.voter_password_entry.delete(0, tk.END)
            self.refresh_voters_list()
            self.refresh_statistics()
        else:
            messagebox.showerror("Error", message)
    
    def refresh_candidates_list(self):
        """Refresh the candidates list"""
        # Clear existing items
        for item in self.candidates_tree.get_children():
            self.candidates_tree.delete(item)
        
        # Add current candidates
        candidates = self.voting_system.get_candidates()
        for candidate in candidates:
            self.candidates_tree.insert('', 'end', values=candidate)
    
    def refresh_voters_list(self):
        """Refresh the voters list"""
        # Clear existing items
        for item in self.voters_tree.get_children():
            self.voters_tree.delete(item)
        
        # Add current voters
        voters = self.voting_system.get_all_voters()
        for voter in voters:
            voter_id, name, has_voted, reg_date = voter
            status = "Yes" if has_voted else "No"
            self.voters_tree.insert('', 'end', values=(voter_id, name, status, reg_date))
    
    def refresh_results(self):
        """Refresh the results display"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add current results
        results = self.voting_system.get_voting_results()
        total_votes = self.voting_system.get_statistics()['total_votes']
        
        for rank, (candidate_id, name, party, vote_count) in enumerate(results, 1):
            percentage = (vote_count / max(total_votes, 1)) * 100
            party_display = party if party else "Independent"
            self.results_tree.insert('', 'end', values=(rank, name, party_display, vote_count, f"{percentage:.1f}%"))
    
    def refresh_recent_activity(self):
        """Refresh the recent activity display"""
        if not hasattr(self, 'activity_tree'):
            return
            
        # Clear existing items
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        # Add recent votes
        recent_votes = self.voting_system.get_recent_votes(10)
        if recent_votes:
            for timestamp, candidate_name, party in recent_votes:
                party_display = party if party else "Independent"
                # Format timestamp
                if timestamp:
                    try:
                        from datetime import datetime
                        if isinstance(timestamp, str):
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            formatted_time = dt.strftime('%H:%M:%S')
                        else:
                            formatted_time = str(timestamp)
                    except:
                        formatted_time = str(timestamp)
                else:
                    formatted_time = "Unknown"
                
                self.activity_tree.insert('', 'end', values=(formatted_time, candidate_name, party_display))
    
    def start_auto_refresh(self):
        """Start auto-refresh of results"""
        self.auto_refresh_job = None
        self.schedule_auto_refresh()
    
    def schedule_auto_refresh(self):
        """Schedule the next auto-refresh"""
        if hasattr(self, 'auto_refresh_var') and self.auto_refresh_var.get():
            # Refresh data
            self.refresh_results()
            self.refresh_recent_activity()
            
            # Schedule next refresh in 5 seconds
            self.auto_refresh_job = self.root.after(5000, self.schedule_auto_refresh)
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh on/off"""
        if self.auto_refresh_var.get():
            self.schedule_auto_refresh()
        else:
            if hasattr(self, 'auto_refresh_job') and self.auto_refresh_job:
                self.root.after_cancel(self.auto_refresh_job)
                self.auto_refresh_job = None
    
    def refresh_statistics(self):
        """Refresh the statistics display"""
        # Get updated statistics
        stats = self.voting_system.get_statistics()
        
        # Update the statistics cards if they exist
        if hasattr(self, 'current_frame'):
            # Find and update statistics frame
            for widget in self.current_frame.winfo_children():
                if isinstance(widget, tk.LabelFrame) and "System Overview" in str(widget.cget('text')):
                    # Recreate statistics section
                    widget.destroy()
                    self.create_statistics_section()
                    break
    
    def export_results(self):
        """Export results summary"""
        summary = self.voting_system.export_results_summary()
        if summary:
            # Create a new window to display the summary
            export_window = tk.Toplevel(self.root)
            export_window.title("Results Summary")
            export_window.geometry("600x500")
            
            text_widget = scrolledtext.ScrolledText(export_window, font=('Courier', 10))
            text_widget.pack(fill='both', expand=True, padx=10, pady=10)
            text_widget.insert('1.0', summary)
            text_widget.config(state='disabled')
            
            # Save button
            save_btn = tk.Button(
                export_window, 
                text="Save to File", 
                command=lambda: self.save_summary_to_file(summary),
                bg='#27ae60',
                fg='white'
            )
            save_btn.pack(pady=10)
    
    def save_summary_to_file(self, summary):
        """Save summary to a text file"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(summary)
                messagebox.showinfo("Success", f"Summary saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def logout(self):
        """Logout and return to login screen"""
        self.voting_system.logout()
        self.parent_gui.setup_login_screen()