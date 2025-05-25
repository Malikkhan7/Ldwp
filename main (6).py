from flask import Flask, render_template_string, request, jsonify
import subprocess
import threading
import time

app = Flask(__name__)
is_running = False

@app.route('/')
def index():
    return render_template_string("""
    <h2>WhatsApp QR Login & Sender</h2>
    <form action="/start" method="post">
        <input type="text" name="number" placeholder="Target Number with +91" required><br>
        <input type="text" name="message" placeholder="Message" required><br>
        <input type="number" name="delay" placeholder="Delay (seconds)" required><br>
        <button type="submit">Start Sending</button>
    </form>
    """)

@app.route('/start', methods=['POST'])
def start():
    global is_running
    if is_running:
        return "Already sending..."

    number = request.form['number']
    message = request.form['message']
    delay = int(request.form['delay'])

    def send_loop():
        global is_running
        is_running = True
        while is_running:
            subprocess.run(['node', 'send.js', number, message])
            time.sleep(delay)

    threading.Thread(target=send_loop).start()
    return "Started sending messages nonstop!"

@app.route('/stop')
def stop():
    global is_running
    is_running = False
    return "Stopped!"

if __name__ == '__main__':
    app.run(debug=True)
