from flask import Flask, jsonify,request,render_template
import requests
from mysql.connector import connect


con=connect(host='localhost'
            ,port=3306
            ,database='weather_data'
            ,user='root')


app = Flask(__name__)

@app.route('/')
def fun():
    return render_template("index.html")



@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        cur=con.cursor()
        cur.execute("insert into jash values(%s,%s,%s)",(name,email,password))
        con.commit()
        return render_template("index.html")
    else:
        return None


@app.route("/login",methods=["POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        cur=con.cursor()
        cur.execute("SELECT * FROM jash where email=%s and password=%s",(email,password))
        res=cur.fetchall()
        if res:
            return render_template("home.html")
        else:
            return "incorrect password or not logged in"
    else:
        return None


@app.route('/index', methods=["GET","POST"])
def index():
    if request.method == "POST":
        city_name = request.form.get('city')
        r = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city_name+'&appid=6d49cd25afaaeb99378eeb5bf1490176')
        json_object = r.json() 
        temp = int(json_object['main']['temp'])
        humidity = int(json_object['main']['humidity'])
        pressure = int(json_object['main']['pressure'])
        wind = int(json_object['wind']['speed'])
        temperature=str(temp-273.15)


        condition = json_object['weather'][0]['main']
        desc = json_object['weather'][0]['description']
        
        return render_template('home.html',temperature=temperature,pressure=pressure,humidity=humidity,city_name=city_name,condition=condition,wind=wind,desc=desc)
    else:
        return render_template('home.html') 


if __name__ == '__main__':
    app.run(debug=True)