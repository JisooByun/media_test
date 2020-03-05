

from flask import Flask, request,jsonify,render_template
from flask_cors import CORS
import rpy
# import graph_data
app = Flask(__name__)
CORS(app)
@app.route('/')
def introduce():
    return render_template('kt.html')

@app.route('/test',methods = ['POST'])
def hello():
    result =  request.get_json(force = True)
    index = result['index']
    print(index)
    rpy.make_df(index)
    x = rpy.choose_two(index)
    return jsonify(x)

if __name__ == "__main__":
    app.run(debug=True)
# host = '0.0.0.0',port='5000'