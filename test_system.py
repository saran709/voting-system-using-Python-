#!/usr/bin/env python3
# Code created by https://linktr.ee/saran709
"""
Test script for the Offline Voting System
This script validates all core functionality without requiring GUI interaction.
"""

import os
import sys
from database_manager import DatabaseManager
from voting_system import VotingSystem

def test_database_creation():
    """Test database initialization"""
    print("Testing database creation...")
    db = DatabaseManager("test_voting.db")
    
    # Test connection
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    expected_tables = ['voters', 'candidates', 'votes', 'admin']
    
    table_names = [table[0] for table in tables]
    for expected in expected_tables:
        assert expected in table_names, f"Table {expected} not found"
    
    conn.close()
    print("✓ Database creation test passed")
    return db

def test_admin_authentication(db):
    """Test admin authentication"""
    print("Testing admin authentication...")
    
    # Test default admin login
    success = db.authenticate_admin("admin", "admin123")
    assert success, "Default admin authentication failed"
    
    # Test wrong password
    success = db.authenticate_admin("admin", "wrongpassword")
    assert not success, "Admin authentication should fail with wrong password"
    
    print("✓ Admin authentication test passed")

def test_candidate_management(voting_system):
    """Test candidate management"""
    print("Testing candidate management...")
    
    # Add candidates
    success, msg = voting_system.add_candidate("John Doe", "Democratic Party", "Experienced leader")
    assert success, f"Failed to add candidate: {msg}"
    
    success, msg = voting_system.add_candidate("Jane Smith", "Republican Party", "Business background")
    assert success, f"Failed to add candidate: {msg}"
    
    success, msg = voting_system.add_candidate("Bob Johnson", "Independent", "Fresh perspective")
    assert success, f"Failed to add candidate: {msg}"
    
    # Test duplicate candidate
    success, msg = voting_system.add_candidate("John Doe", "Another Party", "Duplicate test")
    assert not success, "Should not allow duplicate candidate names"
    
    # Get candidates
    candidates = voting_system.get_candidates()
    assert len(candidates) == 3, f"Expected 3 candidates, got {len(candidates)}"
    
    print("✓ Candidate management test passed")
    return candidates

def test_voter_registration(voting_system):
    """Test voter registration"""
    print("Testing voter registration...")
    
    # Register voters
    success, msg = voting_system.register_voter("voter001", "Alice Cooper", "password123")
    assert success, f"Failed to register voter: {msg}"
    
    success, msg = voting_system.register_voter("voter002", "Bob Wilson", "mypassword")
    assert success, f"Failed to register voter: {msg}"
    
    success, msg = voting_system.register_voter("voter003", "Carol Davis", "secret456")
    assert success, f"Failed to register voter: {msg}"
    
    # Test duplicate voter ID
    success, msg = voting_system.register_voter("voter001", "Another Alice", "different")
    assert not success, "Should not allow duplicate voter IDs"
    
    # Get voters
    voters = voting_system.get_all_voters()
    assert len(voters) == 3, f"Expected 3 voters, got {len(voters)}"
    
    print("✓ Voter registration test passed")
    return voters

def test_voting_process(voting_system, candidates):
    """Test the voting process"""
    print("Testing voting process...")
    
    # Test voter login and voting
    success, msg, name = voting_system.login_voter("voter001", "password123")
    assert success, f"Voter login failed: {msg}"
    
    # Cast vote for first candidate
    candidate_id = candidates[0][0]
    success, msg = voting_system.cast_vote(candidate_id)
    assert success, f"Vote casting failed: {msg}"
    
    # Test duplicate voting (should fail)
    success, msg = voting_system.cast_vote(candidate_id)
    assert not success, "Should not allow duplicate voting"
    
    # Login second voter and vote
    voting_system.logout()
    success, msg, name = voting_system.login_voter("voter002", "mypassword")
    assert success, f"Second voter login failed: {msg}"
    
    # Vote for second candidate
    candidate_id = candidates[1][0]
    success, msg = voting_system.cast_vote(candidate_id)
    assert success, f"Second vote casting failed: {msg}"
    
    # Login third voter and vote
    voting_system.logout()
    success, msg, name = voting_system.login_voter("voter003", "secret456")
    assert success, f"Third voter login failed: {msg}"
    
    # Vote for first candidate (making it have 2 votes)
    candidate_id = candidates[0][0]
    success, msg = voting_system.cast_vote(candidate_id)
    assert success, f"Third vote casting failed: {msg}"
    
    print("✓ Voting process test passed")

def test_results_and_statistics(voting_system):
    """Test results and statistics"""
    print("Testing results and statistics...")
    
    # Login as admin to view results
    voting_system.logout()
    success, msg = voting_system.login_admin("admin", "admin123")
    assert success, f"Admin login failed: {msg}"
    
    # Get results
    results = voting_system.get_voting_results()
    assert len(results) == 3, f"Expected 3 candidates in results, got {len(results)}"
    
    # Check vote counts (first candidate should have 2 votes, second should have 1)
    first_candidate_votes = results[0][3]  # votes are sorted by count desc
    assert first_candidate_votes == 2, f"Expected 2 votes for winning candidate, got {first_candidate_votes}"
    
    # Get statistics
    stats = voting_system.get_statistics()
    assert stats['total_voters'] == 3, f"Expected 3 total voters, got {stats['total_voters']}"
    assert stats['total_votes'] == 3, f"Expected 3 total votes, got {stats['total_votes']}"
    assert stats['voters_who_voted'] == 3, f"Expected 3 voters who voted, got {stats['voters_who_voted']}"
    assert stats['voter_turnout'] == 100.0, f"Expected 100% turnout, got {stats['voter_turnout']}%"
    
    # Test export summary
    summary = voting_system.export_results_summary()
    assert summary is not None, "Export summary should not be None"
    assert "VOTING RESULTS SUMMARY" in summary, "Summary should contain title"
    
    print("✓ Results and statistics test passed")

def test_validation_functions(voting_system):
    """Test validation functions"""
    print("Testing validation functions...")
    
    # Test voter ID validation
    valid, msg = voting_system.validate_voter_id("valid123")
    assert valid, f"Valid voter ID should pass: {msg}"
    
    valid, msg = voting_system.validate_voter_id("")
    assert not valid, "Empty voter ID should fail"
    
    valid, msg = voting_system.validate_voter_id("ab")
    assert not valid, "Short voter ID should fail"
    
    # Test password validation
    valid, msg = voting_system.validate_password("goodpassword")
    assert valid, f"Valid password should pass: {msg}"
    
    valid, msg = voting_system.validate_password("123")
    assert not valid, "Short password should fail"
    
    # Test candidate name validation
    valid, msg = voting_system.validate_candidate_name("Valid Candidate")
    assert valid, f"Valid candidate name should pass: {msg}"
    
    valid, msg = voting_system.validate_candidate_name("")
    assert not valid, "Empty candidate name should fail"
    
    print("✓ Validation functions test passed")

def cleanup_test_database():
    """Clean up test database"""
    try:
        os.remove("test_voting.db")
        print("✓ Test database cleaned up")
    except FileNotFoundError:
        pass

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("OFFLINE VOTING SYSTEM - AUTOMATED TESTS")
    print("=" * 50)
    
    try:
        # Initialize with test database
        db = test_database_creation()
        voting_system = VotingSystem()
        voting_system.db = db  # Use test database
        
        # Login as admin for management operations
        success, msg = voting_system.login_admin("admin", "admin123")
        assert success, f"Initial admin login failed: {msg}"
        
        # Run all tests
        test_admin_authentication(db)
        candidates = test_candidate_management(voting_system)
        voters = test_voter_registration(voting_system)
        test_voting_process(voting_system, candidates)
        test_results_and_statistics(voting_system)
        test_validation_functions(voting_system)
        
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED! ✓")
        print("=" * 50)
        print("\nThe voting system is working correctly!")
        print("\nTest Summary:")
        print(f"• Database: Created with {len(candidates)} candidates and {len(voters)} voters")
        print("• Authentication: Admin and voter login working")
        print("• Voting: All voters successfully cast votes")
        print("• Results: Vote counting and statistics accurate")
        print("• Security: Duplicate voting prevention working")
        print("• Validation: Input validation functions working")
        
        # Display final results
        results = voting_system.get_voting_results()
        print("\nFinal Voting Results:")
        for i, (cid, name, party, votes) in enumerate(results, 1):
            print(f"{i}. {name} ({party}): {votes} votes")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False
    finally:
        cleanup_test_database()
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)