from flask import Flask, render_template
app = Flask(__name__)
 
@app.route("/")
def index():
	page_name="index"
	return render_template('%s.html' % page_name)

def getData(data):
	return None
 
if __name__ == "__main__":
    app.run()