from app import create_app
import sys

try:
    print("Creating app...")
    app = create_app()
    print("App created successfully.")
    print(app.url_map)
    sys.exit(0)
except Exception as e:
    print(f"Failed to create app: {e}")
    sys.exit(1)
