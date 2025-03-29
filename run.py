from app import create_app
import os


if __name__ == "__main__":
    # Run the Flask application using environment-defined host, port, and debug mode
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    flask_app = create_app()
    flask_app.run(host=host, port=port, debug=debug)
