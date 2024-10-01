import os
from flask import Flask, render_template, request, jsonify
from summarizer import generate_campaign_plan

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_campaign_plan', methods=['POST'])
def generate_campaign_plan_route():
    # Get the form data
    district = request.form['district']
    voters = request.form['voters']
    vote_goal = request.form['vote-goal']
    budget = request.form['budget']
    issues = request.form['issues']
    demographics = request.form['demographics']

    try:
        # Call the generate_campaign_plan function to create the campaign plan
        campaign_plan = generate_campaign_plan(district, voters, vote_goal, budget, issues, demographics)
        return jsonify({'success': True, 'plan': campaign_plan})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
