from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure tables exist (redundant if init_db ran, but safe)
        db.create_all()
    print("Starting test server on 8001...")
    # debug=True for errors, use_reloader=False to avoid subprocess issues
    app.run(port=8001, debug=True, use_reloader=False)
