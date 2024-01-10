from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    # messages = Message.query.all()


    if request.method == "GET":
        ordered_messages = Message.query.order_by(Message.created_at).all()
        messages_dict = []
        for each in ordered_messages:
            messages_dict.append(each.to_dict())
        return messages_dict, 200
       
           
    elif request.method == "POST":
        json_dict = request.get_json()
        new_message = Message(
            body = json_dict.get("body"),
            username = json_dict.get("username")
        )
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 200
      
    

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == "PATCH":
        json_dict = request.get_json()
        message_dict = message.to_dict()
        for attr in json_dict:
            setattr(message, attr, json_dict.get(attr))
        db.session.add(message)
        db.session.commit()
        return message.to_dict(), 200
    
       
    elif request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()


if __name__ == '__main__':
    app.run(port=5555)

