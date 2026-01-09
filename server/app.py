from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

# -----------------------------
# ROUTES
# -----------------------------

# GET all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    all_messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in all_messages])

# POST new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data["body"], username=data["username"])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# GET, PATCH, DELETE by id
@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def message_by_id(id):
    message = Message.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(message.to_dict())

    elif request.method == 'PATCH':
        data = request.get_json()
        message.body = data.get("body", message.body)
        db.session.commit()
        return jsonify(message.to_dict())

    elif request.method == 'DELETE':
        # Actually delete the message (required for CodeGrade test)
        db.session.delete(message)
        db.session.commit()
        return '', 204

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == '__main__':
    app.run(port=5555)
