# Code created by https://linktr.ee/saran709
from database_manager import DatabaseManager
from datetime import datetime

class VotingSystem:
    """
    Core voting system logic and business rules
    """
    
    def __init__(self):
        self.db = DatabaseManager()
        self.current_voter = None
        self.is_admin = False
    
    def login_voter(self, voter_id, password):
        """
        Authenticate and login a voter
        Returns: (success, message, voter_name)
        """
        success, voter_name, has_voted = self.db.authenticate_voter(voter_id, password)
        
        if not success:
            return False, "Invalid voter ID or password", None
        
        if has_voted:
            return False, "You have already voted in this election", voter_name
        
        self.current_voter = voter_id
        self.is_admin = False
        return True, f"Welcome {voter_name}!", voter_name
    
    def login_admin(self, admin_id, password):
        """
        Authenticate and login an admin
        Returns: (success, message)
        """
        success = self.db.authenticate_admin(admin_id, password)
        
        if success:
            self.current_voter = None
            self.is_admin = True
            return True, "Admin login successful"
        else:
            return False, "Invalid admin credentials"
    
    def logout(self):
        """Logout current user"""
        self.current_voter = None
        self.is_admin = False
    
    def cast_vote(self, candidate_id):
        """
        Cast a vote for the specified candidate
        Returns: (success, message)
        """
        if not self.current_voter:
            return False, "Please login first"
        
        if not self.is_eligible_to_vote():
            return False, "You are not eligible to vote"
        
        # Verify candidate exists
        candidates = self.db.get_all_candidates()
        candidate_exists = any(c[0] == candidate_id for c in candidates)
        
        if not candidate_exists:
            return False, "Invalid candidate selection"
        
        try:
            # Cast the vote
            self.db.cast_vote(candidate_id)
            
            # Mark voter as having voted
            self.db.mark_voter_as_voted(self.current_voter)
            
            return True, "Your vote has been cast successfully!"
        
        except Exception as e:
            return False, f"Error casting vote: {str(e)}"
    
    def is_eligible_to_vote(self):
        """Check if current voter is eligible to vote"""
        if not self.current_voter:
            return False
        
        # Check if voter has already voted by querying the database directly
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT has_voted FROM voters WHERE voter_id = ?", (self.current_voter,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return not result[0]  # Return True if has_voted is False
        return False
    
    def get_candidates(self):
        """Get all available candidates"""
        return self.db.get_all_candidates()
    
    def get_voting_results(self):
        """Get current voting results (admin only)"""
        if not self.is_admin:
            return None
        
        return self.db.get_voting_results()
    
    def add_candidate(self, name, party="", description=""):
        """Add a new candidate (admin only)"""
        if not self.is_admin:
            return False, "Admin access required"
        
        return self.db.add_candidate(name, party, description)
    
    def remove_candidate(self, candidate_id):
        """Remove a candidate (admin only)"""
        if not self.is_admin:
            return False, "Admin access required"
        
        success = self.db.remove_candidate(candidate_id)
        if success:
            return True, "Candidate removed successfully"
        else:
            return False, "Candidate not found"
    
    def register_voter(self, voter_id, name, password):
        """Register a new voter (admin only)"""
        if not self.is_admin:
            return False, "Admin access required"
        
        return self.db.register_voter(voter_id, name, password)
    
    def get_all_voters(self):
        """Get all registered voters (admin only)"""
        if not self.is_admin:
            return None
        
        return self.db.get_all_voters()
    
    def get_statistics(self):
        """Get voting statistics"""
        return self.db.get_statistics()
    
    def get_recent_votes(self, limit=10):
        """Get recent votes (admin only)"""
        if not self.is_admin:
            return None
        
        return self.db.get_recent_votes(limit)
    
    def validate_voter_id(self, voter_id):
        """Validate voter ID format"""
        if not voter_id or len(voter_id.strip()) == 0:
            return False, "Voter ID cannot be empty"
        
        if len(voter_id) < 3:
            return False, "Voter ID must be at least 3 characters long"
        
        # Check for valid characters (alphanumeric)
        if not voter_id.replace('_', '').replace('-', '').isalnum():
            return False, "Voter ID can only contain letters, numbers, hyphens, and underscores"
        
        return True, "Valid voter ID"
    
    def validate_password(self, password):
        """Validate password strength"""
        if not password or len(password) < 4:
            return False, "Password must be at least 4 characters long"
        
        return True, "Valid password"
    
    def validate_candidate_name(self, name):
        """Validate candidate name"""
        if not name or len(name.strip()) == 0:
            return False, "Candidate name cannot be empty"
        
        if len(name.strip()) < 2:
            return False, "Candidate name must be at least 2 characters long"
        
        return True, "Valid candidate name"
    
    def get_current_user_info(self):
        """Get information about current logged-in user"""
        if self.is_admin:
            return {"type": "admin", "id": "admin"}
        elif self.current_voter:
            return {"type": "voter", "id": self.current_voter}
        else:
            return {"type": "none", "id": None}
    
    def export_results_summary(self):
        """Export a summary of voting results"""
        if not self.is_admin:
            return None
        
        results = self.get_voting_results()
        stats = self.get_statistics()
        
        summary = []
        summary.append("=" * 50)
        summary.append("VOTING RESULTS SUMMARY")
        summary.append("=" * 50)
        summary.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("")
        
        summary.append("STATISTICS:")
        summary.append(f"Total Registered Voters: {stats['total_voters']}")
        summary.append(f"Total Candidates: {stats['total_candidates']}")
        summary.append(f"Total Votes Cast: {stats['total_votes']}")
        summary.append(f"Voter Turnout: {stats['voter_turnout']:.1f}%")
        summary.append("")
        
        summary.append("RESULTS:")
        summary.append("-" * 30)
        
        for i, (candidate_id, name, party, vote_count) in enumerate(results, 1):
            party_str = f" ({party})" if party else ""
            percentage = (vote_count / max(stats['total_votes'], 1)) * 100
            summary.append(f"{i}. {name}{party_str}: {vote_count} votes ({percentage:.1f}%)")
        
        summary.append("=" * 50)
        
        return "\n".join(summary)