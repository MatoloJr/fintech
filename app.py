from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fintech_app.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # Add other fields as needed

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    # Add other fields as needed

# Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment

user_schema = UserSchema()
users_schema = UserSchema(many=True)
payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route('/payment', methods=['POST'])
def add_payment():
    amount = request.json['amount']
    description = request.json.get('description')
    new_payment = Payment(amount=amount, description=description)
    db.session.add(new_payment)
    db.session.commit()
    return payment_schema.jsonify(new_payment)

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return payments_schema.jsonify(payments)

if __name__ == '__main__':
    app.run(debug=True)
