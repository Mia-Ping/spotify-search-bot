import unittest
import requests
import json
import os
import time

class DeployedAppTests(unittest.TestCase):
    """Test cases for the deployed Spotify Music Search Bot"""
    
    def setUp(self):
        """Set up test variables"""
        # Replace with your actual deployed URL
        self.base_url = "https://spotify-search-bot.onrender.com"
        self.session = requests.Session()
    
    def test_homepage_loads(self):
        """Test that the homepage loads correctly"""
        response = self.session.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Spotify Music Search Bot", response.text)
        self.assertIn("Login with Spotify", response.text)
    
    def test_login_redirect(self):
        """Test that the login endpoint redirects to Spotify"""
        response = self.session.get(f"{self.base_url}/login", allow_redirects=False)
        self.assertIn(response.status_code, [301, 302, 303, 307])  # Any redirect status code
        redirect_url = response.headers.get('Location')
        self.assertIsNotNone(redirect_url)
        self.assertIn("accounts.spotify.com", redirect_url)
        self.assertIn("authorize", redirect_url)
    
    def test_api_endpoints_require_auth(self):
        """Test that API endpoints require authentication"""
        # Test search endpoint
        response = self.session.get(f"{self.base_url}/search?query=test")
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.text)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Not authenticated")
        
        # Test identify endpoint
        response = self.session.post(f"{self.base_url}/identify")
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.text)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Not authenticated")
        
        # Test match-humming endpoint
        response = self.session.post(f"{self.base_url}/match-humming")
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.text)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Not authenticated")
        
        # Test add-to-liked endpoint
        response = self.session.post(
            f"{self.base_url}/add-to-liked",
            json={"track_id": "test"},
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.text)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Not authenticated")
    
    def test_static_files_load(self):
        """Test that static files load correctly"""
        # Test CSS file
        response = self.session.get(f"{self.base_url}/static/css/style.css")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/css", response.headers.get('Content-Type', ''))
        
        # Test JavaScript file
        response = self.session.get(f"{self.base_url}/static/js/app.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn("javascript", response.headers.get('Content-Type', ''))
    
    def test_server_response_time(self):
        """Test that the server responds within a reasonable time"""
        start_time = time.time()
        response = self.session.get(self.base_url)
        end_time = time.time()
        
        response_time = end_time - start_time
        self.assertLess(response_time, 5.0)  # Response should be under 5 seconds
        
if __name__ == '__main__':
    unittest.main()
