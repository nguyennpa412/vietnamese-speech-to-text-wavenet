from flask import Flask, render_template, request
app = Flask(__name__, template_folder='./')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def recognizeFile():
    filepath = request.form['filepath']

if __name__ == '__main__':
    app.run()
