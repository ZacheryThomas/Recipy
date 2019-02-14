from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/submit', methods=['POST']) #allow POST requests
def form_example():
    foods = request.form.get('food')
    return 'You entered {}'.format(foods)

@app.route('/result')
def result():
    return render_template('index.html', iframe_source='www.google.com')

@app.route('/')
def main():
    return '''<form method="POST" action="/submit">
                List Foods: <input type="text" name="foods"><br>
                <input type="submit" value="Submit"><br>
              </form>'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')