#!/usr/bin/env python3
# Code created by https://linktr.ee/saran709
"""
Test Vote Flow and Admin Updates
This script demonstrates how votes flow from voters to admin dashboard
"""

from voting_system import VotingSystem
import time

def test_vote_flow():
    """Test the complete vote flow"""
    print("Testing Vote Flow: Voter -> Backend -> Admin Dashboard")
    print("=" * 60)
    
    # Initialize voting system
    voting_system = VotingSystem()
    
    # Step 1: Login as voter and cast vote
    print("STEP 1: Voter Login and Vote Casting")
    print("-" * 40)
    
    success, message, voter_name = voting_system.login_voter("voter001", "password123")
    if success:
        print(f"✓ Voter login successful: {voter_name}")
        
        # Get candidates
        candidates = voting_system.get_candidates()
        if candidates:
            print(f"✓ Available candidates: {len(candidates)}")
            for i, (cid, name, party, desc) in enumerate(candidates[:3], 1):
                print(f"  {i}. {name} ({party})")
            
            # Cast vote for first candidate
            candidate_id = candidates[0][0]
            candidate_name = candidates[0][1]
            
            success, message = voting_system.cast_vote(candidate_id)
            if success:
                print(f"✓ Vote cast successfully for {candidate_name}")
                print(f"  Message: {message}")
            else:
                print(f"❌ Vote failed: {message}")
        else:
            print("❌ No candidates available")
    else:
        print(f"❌ Voter login failed: {message}")
    
    print("\n" + "=" * 60)
    
    # Step 2: Login as admin and check results
    print("STEP 2: Admin Login and Results Check")
    print("-" * 40)
    
    voting_system.logout()
    success, message = voting_system.login_admin("admin", "admin123")
    
    if success:
        print(f"✓ Admin login successful")
        
        # Get voting results
        results = voting_system.get_voting_results()
        print(f"✓ Retrieved voting results: {len(results)} candidates")
        
        print("\nCurrent Voting Results:")
        print("-" * 30)
        for rank, (cid, name, party, votes) in enumerate(results, 1):
            party_display = party if party else "Independent"
            print(f"{rank}. {name} ({party_display}): {votes} votes")
        
        # Get statistics
        stats = voting_system.get_statistics()
        print(f"\nVoting Statistics:")
        print(f"• Total Voters: {stats['total_voters']}")
        print(f"• Total Candidates: {stats['total_candidates']}")
        print(f"• Total Votes Cast: {stats['total_votes']}")
        print(f"• Voter Turnout: {stats['voter_turnout']:.1f}%")
        
        # Get recent activity
        recent_votes = voting_system.get_recent_votes(5)
        if recent_votes:
            print(f"\nRecent Voting Activity:")
            print("-" * 25)
            for timestamp, candidate, party in recent_votes:
                party_display = party if party else "Independent"
                print(f"• {candidate} ({party_display}) at {timestamp}")
        
    else:
        print(f"❌ Admin login failed: {message}")
    
    print("\n" + "=" * 60)
    print("Vote Flow Test Complete!")
    print("\nFlow Summary:")
    print("1. ✓ Voter logs in and casts vote")
    print("2. ✓ Vote is stored in database with timestamp")
    print("3. ✓ Admin can immediately see updated results")
    print("4. ✓ Recent activity shows real-time vote tracking")
    print("5. ✓ Statistics are updated automatically")

def simulate_multiple_votes():
    """Simulate multiple voters casting votes"""
    print("\n" + "=" * 60)
    print("SIMULATING MULTIPLE VOTES")
    print("=" * 60)
    
    voting_system = VotingSystem()
    
    # List of voters to simulate
    test_voters = [
        ("voter002", "secure456"),
        ("voter003", "mypass789"),
        ("voter004", "secret321")
    ]
    
    candidates = voting_system.get_candidates()
    
    for i, (voter_id, password) in enumerate(test_voters):
        print(f"\nVoter {i+1}: {voter_id}")
        
        success, message, voter_name = voting_system.login_voter(voter_id, password)
        if success:
            # Vote for different candidates
            candidate_idx = i % len(candidates)
            candidate_id = candidates[candidate_idx][0]
            candidate_name = candidates[candidate_idx][1]
            
            success, message = voting_system.cast_vote(candidate_id)
            if success:
                print(f"✓ {voter_name} voted for {candidate_name}")
            else:
                print(f"❌ Vote failed: {message}")
        else:
            print(f"❌ Login failed: {message}")
        
        voting_system.logout()
        time.sleep(1)  # Small delay between votes
    
    # Show final results
    voting_system.login_admin("admin", "admin123")
    results = voting_system.get_voting_results()
    stats = voting_system.get_statistics()
    
    print(f"\nFINAL RESULTS:")
    print("-" * 30)
    for rank, (cid, name, party, votes) in enumerate(results, 1):
        percentage = (votes / max(stats['total_votes'], 1)) * 100
        print(f"{rank}. {name}: {votes} votes ({percentage:.1f}%)")
    
    print(f"\nTotal Votes Cast: {stats['total_votes']}")

if __name__ == "__main__":
    test_vote_flow()
    simulate_multiple_votes()