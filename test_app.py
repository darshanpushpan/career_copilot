#!/usr/bin/env python3
"""
Simple test script to verify Flask app is working correctly
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_app():
    """Test that the Flask app is configured correctly"""
    with app.test_client() as client:
        # Test the main route
        response = client.get('/')
        print(f"Main route status: {response.status_code}")
        print(f"Response contains expected content: {'Career Copilot' in response.get_data(as_text=True)}")

        # Test the analyze route (should return error for missing data)
        response = client.post('/analyze', json={})
        print(f"Analyze route status: {response.status_code}")
        print(f"Analyze route returns JSON: {response.is_json}")

if __name__ == '__main__':
    test_app()
