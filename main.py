import os
import tkinter as tk
import threading
from PIL import Image, ImageTk
from flask import Flask, jsonify, request
from markupsafe import escape

from board_manager import Scoreboard
from image_manager import ScoreboardImage

# Create a Flask web server
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
counter = 0

scoreboard = Scoreboard()

image = ScoreboardImage("scoreboard.png", scoreboard)

@app.route('/upload/<usage>', methods=['POST'])
def upload_base(usage):
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], escape(usage) + os.path.splitext(filename)[1])
        file.save(file_path)
        im = Image.open(file_path)
        im.save(os.path.join(app.config['UPLOAD_FOLDER'], escape(usage) + '.png'))
        im.close()
        os.remove(file_path)
        return jsonify({"message": "Image uploaded successfully", "file_path": file_path}), 200

    return jsonify({"error": "Failed to upload image"}), 500

@app.route('/set/state/<state>', methods=['GET'])
def set_state(state):
    global scoreboard
    scoreboard.set_state(state)
    out = str(scoreboard.get_state())
    refresh_image()
    return out

@app.route('/set/score/<team>/<by>', methods=['GET'])
def score(team, by):
    global scoreboard
    out = str(scoreboard.score(team, int(by)))
    refresh_image()
    return out

@app.route('/set/foul/<team>/<by>', methods=['GET'])
def foul(team, by):
    global scoreboard
    scoreboard.foul(team, int(by))
    out = str(scoreboard.get_fouls(team))
    refresh_image()
    return out

@app.route('/set/player_foul/<team>/<player>/<by>', methods=['GET'])
def player_foul(team, player, by):
    global scoreboard
    scoreboard.player_foul(team, int(player), int(by))
    out = str(scoreboard.get_player_fouls(team, player))
    refresh_image()
    return out

@app.route('/get/score/<team>', methods=['GET'])
def get_count(team):
    return str(scoreboard.get_score(team))

@app.route('/get/fouls/<team>', methods=['GET'])
def get_fouls(team):
    return str(scoreboard.get_fouls(team))

@app.route('/get/player_fouls/<team>/<player>', methods=['GET'])
def get_player_fouls(team, player):
    return str(scoreboard.get_player_fouls(team, int(player)))


def run_flask():
    # Run the Flask web server in a separate thread
    app.run(debug=False, use_reloader=False)

def refresh_image():
    # A Function to refresh the scoreboard image on the panel object
    global panel
    global image
    global scoreboard
    img = ImageTk.PhotoImage(image.update_scoreboard(scoreboard))
    panel.configure(image=img)
    panel.image = img

def start_gui():
    # Create the Tkinter window
    global window
    global panel
    window = tk.Tk()
    window.title("Counter Application")
    window.attributes('-fullscreen', True)
    window.configure(borderwidth=0)
    window.configure(bg='lime')
    window.config(cursor='none')

    # Create a tkinter object to display the scoreboard image
    img = ImageTk.PhotoImage(image.update_scoreboard(scoreboard))
    panel = tk.Label(window, image=img, anchor="se", borderwidth=0)
    panel.pack(side="bottom")

    window.mainloop()

if __name__ == "__main__":
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the Tkinter GUI
    start_gui()
