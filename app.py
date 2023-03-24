"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake




app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

def serialize_cupcake(cupcake):
    """serilize cupcake data so can be used as json"""

    return {
        "id": cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }


@app.route('/api/cupcakes')
def get_cupcakes():
    """returns all the data of cupcakes as JSON"""

    cupcakes = Cupcake.query.all()
    serilized = [serialize_cupcake(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes = serilized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """returns data to single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serilized = serialize_cupcake(cupcake)

    return jsonify(cupcake = serilized)

@app.route('/api/cupcakes', methods=['POST'])
def post_cupcake():
    """posts cupcake to db and returns json"""

    flavor = request.json['flavor']
    image = request.json['image']
    rating = request.json['rating']
    size = request.json['size']

    cupcake = Cupcake(flavor=flavor, image= image, rating = rating, size = size)
    db.session.add(cupcake)
    db.session.commit()
    serilized = serialize_cupcake(cupcake)

    return (jsonify(cupcake = serilized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def edit_cupcake(cupcake_id):
    """edit cupcake using PATCH"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.image = request.json.get('image',cupcake.image)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.size = request.json.get('size', cupcake.size)

    db.session.commit()

    return jsonify(cupcake = serialize_cupcake(cupcake))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """DELETE cupcake using DELETE"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = "Deleted")




