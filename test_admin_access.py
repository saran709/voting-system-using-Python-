#!/usr/bin/env python3
# Code created by https://linktr.ee/saran709
"""
Test Admin Access
Quick test to verify admin login and access to admin functions.
"""

from voting_system import VotingSystem

def test_admin_access():
    """Test admin login and access to admin functions"""
    print("Testing Admin Access...")
    print("=" * 40)
    
    # Initialize voting system
    voting_system = VotingSystem()
    
    # Test admin login
    print("1. Testing admin login...")
    success, message = voting_system.login_admin("admin", "admin123")
    
    if success:
        print(f"✓ Admin login successful: {message}")
        print(f"✓ Admin status: {voting_system.is_admin}")
    else:
        print(f"❌ Admin login failed: {message}")
        return False
    
    # Test add candidate access
    print("\n2. Testing add candidate access...")
    success, message = voting_system.add_candidate("Test Candidate", "Test Party", "Test Description")
    
    if success:
        print(f"✓ Add candidate successful: {message}")
    else:
        print(f"❌ Add candidate failed: {message}")
    
    # Test register voter access
    print("\n3. Testing register voter access...")
    success, message = voting_system.register_voter("test123", "Test Voter", "testpass")
    
    if success:
        print(f"✓ Register voter successful: {message}")
    else:
        print(f"❌ Register voter failed: {message}")
    
    # Test get results access
    print("\n4. Testing get results access...")
    results = voting_system.get_voting_results()
    
    if results is not None:
        print(f"✓ Get results successful: Found {len(results)} candidates")
    else:
        print("❌ Get results failed: No access")
    
    # Test get all voters access
    print("\n5. Testing get all voters access...")
    voters = voting_system.get_all_voters()
    
    if voters is not None:
        print(f"✓ Get voters successful: Found {len(voters)} voters")
    else:
        print("❌ Get voters failed: No access")
    
    print("\n" + "=" * 40)
    print("Admin access test completed!")
    
    return True

if __name__ == "__main__":
    test_admin_access()