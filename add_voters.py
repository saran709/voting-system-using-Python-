#!/usr/bin/env python3
# Code created by https://linktr.ee/saran709
"""
Add 10 voters to the voting system database
This script adds 10 specific voters with their details and passwords.
"""

from voting_system import VotingSystem

def add_10_voters():
    """Add 10 voters with detailed information"""
    print("Adding 10 voters to the Offline Voting System...")
    
    # Initialize the voting system
    voting_system = VotingSystem()
    
    # Login as admin
    success, msg = voting_system.login_admin("admin", "admin123")
    if not success:
        print(f"Error: Failed to login as admin: {msg}")
        return False
    
    print("✓ Admin login successful")
    
    # Define 10 voters with their details
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
    
    print(f"\nRegistering {len(voters_data)} voters...")
    print("-" * 60)
    
    successful_registrations = 0
    failed_registrations = 0
    
    for i, (voter_id, name, password) in enumerate(voters_data, 1):
        success, msg = voting_system.register_voter(voter_id, name, password)
        if success:
            print(f"✓ {i:2d}. Registered: {voter_id} | {name}")
            successful_registrations += 1
        else:
            print(f"⚠ {i:2d}. Failed: {voter_id} | {name} | Reason: {msg}")
            failed_registrations += 1
    
    # Display results
    print("\n" + "=" * 60)
    print("VOTER REGISTRATION COMPLETE!")
    print("=" * 60)
    print(f"✓ Successfully registered: {successful_registrations} voters")
    if failed_registrations > 0:
        print(f"⚠ Failed registrations: {failed_registrations} voters")
    
    # Show system statistics
    stats = voting_system.get_statistics()
    print(f"\nCurrent System Status:")
    print(f"• Total Registered Voters: {stats['total_voters']}")
    print(f"• Total Candidates: {stats['total_candidates']}")
    print(f"• System Status: Ready for voting")
    
    # Display voter login credentials
    print(f"\n📋 VOTER LOGIN CREDENTIALS:")
    print("-" * 60)
    print(f"{'#':<3} {'Voter ID':<12} {'Password':<15} {'Full Name'}")
    print("-" * 60)
    
    for i, (voter_id, name, password) in enumerate(voters_data, 1):
        print(f"{i:2d}. {voter_id:<12} {password:<15} {name}")
    
    print("\n💡 Instructions:")
    print("1. Run 'python main.py' to start the voting application")
    print("2. Use any of the above voter credentials to login")
    print("3. Admin login: Contact system administrator for credentials")
    
    return True

def main():
    """Main function"""
    print("Offline Voting System - Add 10 Voters")
    print("=" * 50)
    
    if add_10_voters():
        print("\n✅ All voters added successfully!")
    else:
        print("\n❌ Failed to add voters!")

if __name__ == "__main__":
    main()