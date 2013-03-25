from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/<name>")
def hello(name=None):
    return render_template("hello.html", name = name)

#Primera linea agregada por Cathe
#Corremos el servidor
if __name__ == "__main__":
    app.run()    
