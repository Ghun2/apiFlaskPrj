from flask import Flask, request, jsonify
from models import User
import models


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:0000@localhost/DRSLR_V2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.init_app(app)


def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))


@app.route('/')
def hello_world():
    user_res = User.query.first()
    # for val in user_res:
    #     print(user_res)
    print(dump(user_res))
    print(user_res.__dict__)
    # print(user_res.user_name)
    return ''

@app.route('/user/<value>')
def hello_user(value):
    return 'hi jihun! and {0}'.format(value)

@app.route('/userlogin',methods=['POST'])
def userLogin():
    user = request.get_json()
    return jsonify(user)

@app.route('/enviroments/<lang>')
def enviroments(lang):
    return jsonify({"lang":lang})


if __name__ == '__main__':
    app.run(debug=True)

