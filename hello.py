from flask import Flask,render_template,url_for,request
import folium as fo
import googlemaps
import sqlite3 as lite
app=Flask(__name__)

gmaps_key = "IJUSTCHANGEDTHISTOPREVENTHACKFROMOTHERS"
gmaps = googlemaps.Client(key = gmaps_key)
database_filename='C:/Users/user/Desktop/python/flask/db/hello.db'
@app.route('/',methods=['GET','POST'])
def main():
	return render_template('main.html',message="")

@app.route('/index',methods=['POST','GET'])
def index():
	conn = lite.connect(database_filename)
	cs = conn.cursor()
	idd=request.form['id']
	pwd=request.form['pwd']
	log_name=cs.execute("SELECT * FROM login;").fetchall()
	print(log_name)
	for x in log_name:
		if(x[0]==idd and x[1]==pwd):
			print(x)
			return render_template('hello.html',name=x[2])
	cs.close()
	conn.close()
	return render_template('main.html',message="You've got the wrong id or password!!")

@app.route('/data',methods=['GET','POST'])
def data():
	place=request.form['place']
	if(place==''):
		lat=37
		lng=127
		zoom=7;
	else:
		temp = gmaps.geocode(place,language = 'ko')
		temp_loc=temp[0].get('geometry')
		lat=temp_loc['location']['lat']
		lng=temp_loc['location']['lng']
		zoom=17
	map=fo.Map(location=[lat,lng],zoom_start=zoom)
	map.save('C:/Users/user/Desktop/python/flask/templates/new.html')
	return render_template('new.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/register/loading',methods=['POST'])
def reg():
	conn = lite.connect(database_filename)
	cs = conn.cursor()
	a=request.form['a']
	b=request.form['b']
	c=request.form['c']
	cs.execute("INSERT INTO login VALUES(?,?,?);",(a,b,c))
	conn.commit()
	cs.close()
	conn.close()
	return render_template('complete.html')

if __name__ == '__main__':
	app.run(debug=True)