#!/usr/bin/env python3
# Code created by https://linktr.ee/saran709
"""
Setup script for the Offline Voting System
This script initializes the system with sample candidates and voters for demonstration.
"""

from database_manager import DatabaseManager
from voting_system import VotingSystem

def setup_sample_data():
    """Setup the voting system with sample data"""
    print("Setting up Offline Voting System with sample data...")
    
    # Initialize the voting system
    voting_system = VotingSystem()
    
    # Login as admin
    success, msg = voting_system.login_admin("admin", "admin123")
    if not success:
        print(f"Error: Failed to login as admin: {msg}")
        return False
    
    print("✓ Admin login successful")
    
    # Add sample candidates
    candidates_data = [
        ("Alice Johnson", "Progressive Party", "Advocate for education and healthcare reform"),
        ("Robert Chen", "Conservative Alliance", "Focus on economic growth and job creation"),
        ("Maria Rodriguez", "Green Movement", "Environmental protection and sustainable development"),
        ("David Kim", "Independent", "Technology innovation and digital governance"),
        ("Sarah Williams", "Unity Party", "Bringing communities together through inclusive policies")
    ]
    
    print("\nAdding sample candidates...")
    for name, party, description in candidates_data:
        success, msg = voting_system.add_candidate(name, party, description)
        if success:
            print(f"✓ Added candidate: {name} ({party})")
        else:
            print(f"⚠ Failed to add {name}: {msg}")
    
    # Add sample voters - 10 detailed voter accounts
    voters_data = [
        ("voter001", "John Smith", "password123"),
        ("voter002", "Emma Davis", "secure456"), 
        ("voter003", "Michael Brown", "mypass789"),
        ("voter004", "Lisa Wilson", "secret321"),
        ("voter005", "James Taylor", "vote2024"),
        ("voter006", "Sarah Johnson", "strongpass1"),
        ("voter007", "Robert Martinez", "myvoice2024"),
        ("voter008", "Jennifer Lee", "democracy99"),
        ("voter009", "Christopher Garcia", "elect2024"),
        ("voter010", "Amanda Rodriguez", "citizen123")
    ]
    
    print("\nRegistering sample voters...")
    for voter_id, name, password in voters_data:
        success, msg = voting_system.register_voter(voter_id, name, password)
        if success:
            print(f"✓ Registered voter: {voter_id} ({name})")
        else:
            print(f"⚠ Failed to register {voter_id}: {msg}")
    
    # Display system statistics
    stats = voting_system.get_statistics()
    print("\n" + "=" * 50)
    print("SETUP COMPLETE!")
    print("=" * 50)
    print(f"Total Candidates: {stats['total_candidates']}")
    print(f"Total Registered Voters: {stats['total_voters']}")
    print(f"System Status: Ready for voting")
    
    print("\nADMIN LOGIN:")
    print("Username: admin")
    print("Password: [Default password set during installation]")
    print("Note: Change default admin password for security")
    
    print("\nALL VOTER LOGIN CREDENTIALS:")
    print("-" * 60)
    print(f"{'#':<3} {'Voter ID':<12} {'Password':<15} {'Full Name'}")
    print("-" * 60)
    for i, (voter_id, name, password) in enumerate(voters_data, 1):
        print(f"{i:2d}. {voter_id:<12} {password:<15} {name}")
    
    print(f"\nTotal Voters Added: {len(voters_data)}")
    print("\nTo start the voting system:")
    print("python main.py")
    
    return True

def reset_database():
    """Reset the database by removing the existing one"""
    import os
    try:
        if os.path.exists("voting_database.db"):
            os.remove("voting_database.db")
            print("✓ Existing database removed")
        else:
            print("ℹ No existing database found")
        return True
    except Exception as e:
        print(f"Error removing database: {e}")
        return False

def main():
    """Main setup function"""
    print("Offline Voting System - Setup Script")
    print("=" * 40)
    
    choice = input("Do you want to reset the database? (y/N): ").strip().lower()
    if choice in ['y', 'yes']:
        if not reset_database():
            return
    
    if setup_sample_data():
        print("\n✓ Setup completed successfully!")
    else:
        print("\n❌ Setup failed!")

if __name__ == "__main__":
    main()