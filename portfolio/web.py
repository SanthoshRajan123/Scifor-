from flask import Flask

web = Flask(__name__)
@web.route('/')

def home():
    return "My First Website"

@web.route('/about/')

def about():
    return "about my page"

if __name__ == '__main__':
    web.run(debug=True)