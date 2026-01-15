import requests
import json

BASE_URL = 'http://127.0.0.1:8001'

def test_add_bookmark():
    print("Testing Add Bookmark...")
    payload = {
        "paper_id": "1234.5678",
        "title": "Test Paper",
        "authors": "Test Author",
        "summary": "This is a test summary.",
        "published": "2023-01-01",
        "pdf_link": "http://example.com/pdf",
        "source": "Arxiv",
        "url": "http://example.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/bookmark/add", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("SUCCESS: Bookmark added.")
        elif response.status_code == 200:
             print(f"NOTE: {response.json().get('message')}")
        else:
            print(f"FAILURE: Unexpected status code {response.status_code}")
            print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")

def test_duplicate_bookmark():
    print("\nTesting Duplicate Bookmark...")
    payload = {
        "paper_id": "1234.5678",
        "title": "Test Paper",
        "authors": "Test Author"
    }
    try:
        response = requests.post(f"{BASE_URL}/bookmark/add", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200 and response.json().get('message') == 'Already bookmarked':
            print("SUCCESS: Duplicate correctly handled.")
        else:
            print("FAILURE: Duplicate not handled correctly.")
    except Exception as e:
        print(f"ERROR: {e}")

def test_get_bookmarks():
    print("\nTesting Get Bookmarks HTML...")
    try:
        response = requests.get(f"{BASE_URL}/bookmarks")
        if response.status_code == 200:
            if "Test Paper" in response.text:
                print("SUCCESS: Bookmark found in HTML.")
            else:
                print("FAILURE: Bookmark not found in HTML.")
        else:
             print(f"FAILURE: Status code {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_add_bookmark()
    test_duplicate_bookmark()
    test_get_bookmarks()
