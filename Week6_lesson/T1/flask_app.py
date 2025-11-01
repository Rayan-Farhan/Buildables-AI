from flask import Flask, jsonify, request

app = Flask(__name__)

# storage
todos = [
    {"id": 1, "task": "Complete Project"}
]

# GET Endpoint - Return todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# POST Endpoint - Add todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()

    if not data or 'task' not in data:
        return jsonify({"error": "Missing 'task' field"}), 400

    new_todo = {
        "id": len(todos) + 1,
        "task": data['task']
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

if __name__ == '__main__':
    app.run(debug=True)