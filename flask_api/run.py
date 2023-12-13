from flask import Flask

app = Flask(__name__)

'''
Example that is possible to pass smthg
@app.route("/<number>", methods=['GET', 'POST'])
def hello(number):
    return 'Hello World! {}'.format(number)

'''


@app.route("/", methods=['GET', 'POST'])
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
