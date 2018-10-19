from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    key = request.args.get('key')
    return render_template('captcha.html')


if __name__ == '__main__':
    app.run()
