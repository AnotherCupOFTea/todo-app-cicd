from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/todos")
def list_todos():
    return jsonify(todos)


@app.post("/todos")
def add_todo():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="title is required"), 400
    todo = {"id": len(todos) + 1, "title": title, "done": False}
    todos.append(todo)
    return jsonify(todo), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
