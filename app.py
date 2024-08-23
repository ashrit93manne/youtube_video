from flask import Flask,render_template,request
import sqlite3
import pickle
import sklearn
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact',methods=['GET','POST'])
def contactus():
    if request.method=='POST':
        fname =request.form.get('fullname')
        pno = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        message = request.form.get('message')
        conn = sqlite3.connect('yotube.db')
        cur = conn.cursor()
        cur.execute(f'''
                    INSERT INTO CONTACT VALUES(
                    "{fname}",
                    "{pno}",
                    "{email}",
                    "{address}",
                    "{message}"
                    )
                    ''')
        conn.commit()
        return render_template('msg.html')
    else:
        return render_template('contact.html')
@app.route('/analytical')
def youtube_analysis():
    return render_template('analytical.html')

with open("model.pkl","rb") as model_file:
    model = pickle.load(model_file)

@app.route("/predict",methods = ["GET","POST"])
def predict():
    if request.method == "POST":
        nviews = request.form.get("views")
        ndislikes = request.form.get("dislikes")
        ncomments = request.form.get("comments")
        genre  =request.form.get("genre")
        prediction = model.predict([[float(nviews),float(ndislikes),float(ncomments),float(genre)]])
        return render_template("result.html",prediction=prediction[0])    
    else:
        return render_template("predict.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)