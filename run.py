from app import application
import os

application.debug = False

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(port))