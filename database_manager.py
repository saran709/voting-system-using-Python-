# Code created by https://linktr.ee/saran709
import sqlite3
import hashlib
from datetime import datetime
import os

class DatabaseManager:
    """
    Handles all database operations for the voting system
    """
    
    def __init__(self, db_path="voting_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create voters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voters (
                voter_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                has_voted BOOLEAN DEFAULT FALSE,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create candidates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                party TEXT,
                description TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create votes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER NOT NULL,
                vote_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (candidate_id) REFERENCES candidates (candidate_id)
            )
        ''')
        
        # Create admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                admin_id TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Create default admin if not exists
        self.create_default_admin()
    
    def hash_password(self, password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_admin(self):
        """Create a default admin account"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if admin exists
        cursor.execute("SELECT COUNT(*) FROM admin")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Create default admin (admin/admin123)
            admin_id = "admin"
            password_hash = self.hash_password("admin123")
            cursor.execute(
                "INSERT INTO admin (admin_id, password_hash, name) VALUES (?, ?, ?)",
                (admin_id, password_hash, "System Administrator")
            )
            conn.commit()
        
        conn.close()
    
    # Voter Management
    def register_voter(self, voter_id, name, password):
        """Register a new voter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO voters (voter_id, name, password_hash) VALUES (?, ?, ?)",
                (voter_id, name, password_hash)
            )
            conn.commit()
            return True, "Voter registered successfully"
        except sqlite3.IntegrityError:
            return False, "Voter ID already exists"
        finally:
            conn.close()
    
    def authenticate_voter(self, voter_id, password):
        """Authenticate a voter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT name, has_voted FROM voters WHERE voter_id = ? AND password_hash = ?",
            (voter_id, password_hash)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return True, result[0], result[1]  # Success, name, has_voted
        return False, None, None
    
    def mark_voter_as_voted(self, voter_id):
        """Mark a voter as having voted"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE voters SET has_voted = TRUE WHERE voter_id = ?",
            (voter_id,)
        )
        conn.commit()
        conn.close()
    
    def get_all_voters(self):
        """Get all registered voters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT voter_id, name, has_voted, registration_date FROM voters")
        voters = cursor.fetchall()
        conn.close()
        return voters
    
    # Candidate Management
    def add_candidate(self, name, party="", description=""):
        """Add a new candidate"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO candidates (name, party, description) VALUES (?, ?, ?)",
                (name, party, description)
            )
            conn.commit()
            return True, "Candidate added successfully"
        except sqlite3.IntegrityError:
            return False, "Candidate name already exists"
        finally:
            conn.close()
    
    def get_all_candidates(self):
        """Get all candidates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT candidate_id, name, party, description FROM candidates")
        candidates = cursor.fetchall()
        conn.close()
        return candidates
    
    def remove_candidate(self, candidate_id):
        """Remove a candidate"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM candidates WHERE candidate_id = ?", (candidate_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    # Voting Operations
    def cast_vote(self, candidate_id):
        """Cast a vote for a candidate"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insert vote with current timestamp
        cursor.execute(
            "INSERT INTO votes (candidate_id, vote_timestamp) VALUES (?, CURRENT_TIMESTAMP)",
            (candidate_id,)
        )
        conn.commit()
        conn.close()
        return True
    
    def get_voting_results(self):
        """Get voting results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.candidate_id, c.name, c.party, COUNT(v.vote_id) as vote_count
            FROM candidates c
            LEFT JOIN votes v ON c.candidate_id = v.candidate_id
            GROUP BY c.candidate_id, c.name, c.party
            ORDER BY vote_count DESC
        ''')
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_total_votes(self):
        """Get total number of votes cast"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM votes")
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    # Admin Authentication
    def authenticate_admin(self, admin_id, password):
        """Authenticate an admin"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT name FROM admin WHERE admin_id = ? AND password_hash = ?",
            (admin_id, password_hash)
        )
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    
    # Database Statistics
    def get_statistics(self):
        """Get voting statistics"""
        stats = {}
        stats['total_voters'] = len(self.get_all_voters())
        stats['total_candidates'] = len(self.get_all_candidates())
        stats['total_votes'] = self.get_total_votes()
        stats['voters_who_voted'] = len([v for v in self.get_all_voters() if v[2]])
        stats['voter_turnout'] = (stats['voters_who_voted'] / max(stats['total_voters'], 1)) * 100
        
        return stats
    
    def get_recent_votes(self, limit=10):
        """Get recent votes with candidate information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.vote_timestamp, c.name, c.party
            FROM votes v
            JOIN candidates c ON v.candidate_id = c.candidate_id
            ORDER BY v.vote_timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        recent_votes = cursor.fetchall()
        conn.close()
        return recent_votes