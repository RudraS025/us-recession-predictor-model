from flask import Flask

app = Flask(__name__)

@app.before_first_request
def startup():
    print("App is starting up!")

@app.route('/')
def hello():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)