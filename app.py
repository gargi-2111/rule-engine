from flask import Flask, render_template, request, jsonify
from rule_engine import create_rule, evaluate_rule, combine_rules
import sqlite3
import json

app = Flask(__name__)

# Serve the HTML UI
@app.route('/')
def index():
    return render_template('index.html')

# Route to create a new rule
@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    rule_string = request.json.get('rule_string')
    try:
        ast = create_rule(rule_string)
        store_rule(rule_string, ast)  # Save the rule to the database
        return jsonify({"message": "Rule created successfully!"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

# Route to evaluate a rule
@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')

    ast = load_rule(rule_id)  # Load the AST from the database
    if not ast:
        return jsonify({"error": "Rule not found"}), 404

    result = evaluate_rule(ast, data)
    return jsonify({"result": result}), 200

# Route to combine rules
@app.route('/combine_rules', methods=['POST'])
def api_combine_rules():
    rule_ids = request.json.get('rule_ids')
    
    rules = [load_rule(rule_id) for rule_id in rule_ids]
    combined_ast = combine_rules(rules)
    
    return jsonify({"message": "Rules combined successfully!"})

# Function to store rule in the database
def store_rule(rule_string, ast):
    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()
    
    ast_json = json.dumps(ast.__dict__, default=lambda o: o.__dict__)
    
    cursor.execute('INSERT INTO rules (rule_string, ast_json) VALUES (?, ?)', (rule_string, ast_json))
    conn.commit()
    conn.close()

# Function to load rule by rule_id from the database
def load_rule(rule_id):
    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT ast_json FROM rules WHERE rule_id = ?', (rule_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return json.loads(result[0])
    return None

if __name__ == '__main__':
    app.run(debug=True)
