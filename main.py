from flask import Flask
import os
import threading
from datetime import datetime

thread = threading.Thread(target=os.system, args=("python3 keep_alive.py &",))

app = Flask(__name__)


@app.route("/")
def index():
    return f"I'm alive {datetime.now()}"


if __name__ == "__main__":
    thread.start()
    app.run(host="0.0.0.0", port=80)
