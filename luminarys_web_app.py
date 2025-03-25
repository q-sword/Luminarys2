from flask import Flask, render_template_string, request, send_file
import random
import json
from datetime import datetime

app = Flask(__name__)

class Agent:
    def __init__(self, name, logic_bias, emotion_bias):
        self.name = name
        self.logic_bias = logic_bias
        self.emotion_bias = emotion_bias

class Strategy:
    def __init__(self, name, logic, emotion, justification):
        self.name = name
        self.logic = logic
        self.emotion = emotion
        self.justification = justification
        self.scores = []

    def simulate(self, cycles=5):
        self.scores = [round(random.uniform(0.82, 0.98), 3) for _ in range(cycles)]
        return sum(self.scores) / len(self.scores)

class MetaGuardianBrain:
    def monitor(self, strategy_name, score, justification, sandbox_scores):
        flags = []
        if score < 0.85:
            flags.append("Fallback suggested.")
        if "wisdom" not in justification.lower():
            flags.append("Ethical clarity recommended.")
        if max(sandbox_scores) - min(sandbox_scores) > 0.2:
            flags.append("Volatility detected.")
        return flags

class SynthesisCouncilMind:
    def __init__(self, agents):
        self.agents = agents

    def vote(self, strategy_name, score):
        threshold = 0.85
        votes = {a.name: ("Yes" if score >= threshold and a.logic_bias >= 0.85 else "No") for a in self.agents}
        approval = sum(1 for v in votes.values() if v == "Yes") / len(votes)
        outcome = "Canon-Approved" if approval >= 0.75 else "Rejected"
        return votes, approval, outcome

HTML_FORM = """
<!doctype html>
<title>Luminarys Web System</title>
<h2>Luminarys Strategy Evaluator</h2>
<form method=post>
  Agents: <input type=number name=agents value=3 min=1><br>
  Strategies: <input type=number name=strategies value=3 min=1><br>
  Cycles: <input type=number name=cycles value=5 min=1><br>
  <input type=submit value=Evaluate>
</form>
{% if results %}
  <h3>Results</h3>
  <pre>{{ results }}</pre>
  <a href="/download">📥 Download JSON</a>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = ""
    if request.method == 'POST':
        agents_count = int(request.form['agents'])
        strategy_count = int(request.form['strategies'])
        cycles = int(request.form['cycles'])

        agents = [Agent(f"Agent_{i+1}", round(random.uniform(0.75, 0.95), 2), round(random.uniform(0.65, 0.9), 2)) for i in range(agents_count)]
        strategies = [Strategy(f"Strategy_{i+1}", 0.9, 0.8, "Formulated through iterative wisdom synthesis.") for i in range(strategy_count)]

        sgfi = MetaGuardianBrain()
        council = SynthesisCouncilMind(agents)

        evaluation_log = {"run": datetime.now().isoformat(), "results": []}
        results_text = ""

        for s in strategies:
            avg = s.simulate(cycles)
            flags = sgfi.monitor(s.name, avg, s.justification, s.scores)
            votes, approval, outcome = council.vote(s.name, avg)

            results_text += f"Strategy: {s.name}\nAvg Score: {avg:.3f}\nFlags: {flags}\nOutcome: {outcome} ({approval*100:.1f}%)\n\n"

            evaluation_log["results"].append({
                "strategy": s.name,
                "avg_score": avg,
                "scores": s.scores,
                "flags": flags,
                "outcome": outcome,
                "approval": approval,
                "votes": votes
            })

        with open("luminarys_web_results.json", "w") as f:
            json.dump(evaluation_log, f, indent=4)

        results = results_text

    return render_template_string(HTML_FORM, results=results)

@app.route('/download')
def download():
    return send_file("luminarys_web_results.json", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
