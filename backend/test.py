from flask import Flask, send_from_directory

app = Flask(__name__)

# Define the directory where the images are stored
IMAGE_DIR = 'app/ product/images'

@app.route('/image/<filename>')
def get_image(filename):
    """Returns an image from the given directory."""
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)