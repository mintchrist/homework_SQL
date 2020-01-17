from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return (
        f'/api/v1.0/precipitation<br>'
    f'/api/v1.0/stations<br>'
    f'/api/v1.0/tobs<br>'
    f'/api/v1.0/<start><br/>'
    f'/api/v1.0/<start>/<end><br/>')

if __name__ == "__main__":
    app.run(debug=True)