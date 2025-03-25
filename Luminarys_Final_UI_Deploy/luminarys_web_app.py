from flask import Flask, render_template, request, send_file
import random, json
from datetime import datetime

app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])
def index():
    results = ""
    if request.method == 'POST':
        agents = int(request.form['agents'])
        strategies = int(request.form['strategies'])
        cycles = int(request.form['cycles'])
        results = f"Cognitive simulation: {agents} agents, {strategies} strategies, {cycles} cycles each."
        with open("luminarys_web_results.json", "w") as f:
            json.dump({"log": results, "timestamp": datetime.now().isoformat()}, f, indent=2)
    return render_template("luminarys_template.html", results=results)

@app.route('/download')
def download():
    return send_file("luminarys_web_results.json", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
