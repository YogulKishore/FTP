from flask import Flask, render_template, send_from_directory
import os
import threading
import subprocess

app = Flask(__name__)

# Define the folder you want to share
shared_folder = r'C:\Users\Administrator\Downloads\templates'

def get_localtunnel_url(port):
    command = f'npx localtunnel --port {port}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    url = process.stdout.read().decode('utf-8').strip()
    return url

def start_localtunnel(port):
    get_localtunnel_url(port)

@app.route('/')
def index():
    # Get a list of files in the shared folder
    files = [f for f in os.listdir(shared_folder) if os.path.isfile(os.path.join(shared_folder, f))]

    # Start localtunnel in a separate thread
    threading.Thread(target=start_localtunnel, args=(5000,)).start()

    return render_template('index_localtunnel.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(shared_folder, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
