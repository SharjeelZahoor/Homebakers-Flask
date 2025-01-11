from homebaker import create_app

# Create the Flask app using the factory function
app = create_app()

# Check if this file is being run directly (not imported)
if __name__ == "__main__":
    app.run()
