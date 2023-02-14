from flask import Flask
from flask import request


app= Flask (__name__)
app.secret_key= '@*#%&8'
# above session will be used to encrpyt the user session

@app.route('/') #default route
def home():
    return render_template('index.html')

@app.route('/consultation')
def consultation():
    return render_template('consultation.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/bmi', methods= ['POST', 'GET'])
def bmi():
    if request.method =='POST':
        weight= float (request.form['weight']) #get weight
        height= float (request.form['height'])

        answer = weight/(height*height) # do your maths
    #send the answer back to the teplate
        return render_template('bmi.html', msg=answer)
    else:
        return render_template('bmi.html')
#create a template
#simple interest calculation below
@app.route('/interest', methods= ['POST', 'GET'])
def interest():
    if request.method=='POST':
        principal= float (request.form['principal'])
        rate = float ( request.form ['rate'])
        time= float ( request.form ['time'])

        inte= principal * rate * time
        return render_template('interest.html',
                                inte=inte,
                                principal = principal,
                                rate = rate,
                                time = time)

    else:
        return render_template('interest.html')



# ================== new route
@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method=="POST":
        name=str(request.form ['name'])
        admno=str (request.form['admno'])
        math = float(request.form['math'])
        english=  float(request.form ['english'])
        physics = float(request.form['physics'])
        comment = str(request.form['comment'])

        total= math+ physics+english
        average= total/3

        return render_template('report.html',
                                name=name,
                                admno=admno,
                                total=total,
                                math=math,
                                english=english,
                                physics=physics,
                                comment=comment)

    else:
        return render_template('report.html')

import pymysql
@app.route('/appointments', methods= ['POST', 'GET'])
def appointments():
    if request.method =='POST':
        names = request. form ['names']
        date = request.form ['date']
        time = request.form ['time']
        tel= request.form ['tel']
        doctor= request.form ['doctor']


        conn=pymysql.connect('localhost', 'root', '', 'appledatabase')

        sql= "INSERT INTO appointments (names, date, time, tel, doctor) VALUES (%s, %s, %s, %s, %s)"


        try:
            cursor = conn.cursor()
            cursor.execute (sql, (names,date,time,tel,doctor))
            conn.commit()
            return render_template('appointments.html',
                                msg = 'Your Appointment Received')

        except:
            return render_template('appointments.html',
                                msg='APpointment NOt Received')

    else:
        return render_template('appointments.html')



@app.route('/register', methods= ['POST', 'GET'])
def register():
    if request.method =='POST':
        username=request.form ['username']
        password= request.form ['password']
        gender= request.form ['gender']

        conn=pymysql.connect('localhost', 'root', '', 'appledatabase')

        sql= "INSERT INTO  register (username, password, gender) VALUES (%s, %s, %s)"
        cursor = conn.cursor()

        try:
            cursor = conn.cursor()
            cursor.execute (sql, (username, password,gender))
            conn.commit()
            return render_template('register.html',
                                msg = 'Registration Complete')

        except:
            return render_template('register.html',
                                msg='Registration Failed')

    else:
        return render_template('register.html')


@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method =='POST':
        username=request.form ['username']
        password= request.form ['password']

        conn=pymysql.connect('localhost', 'root', '', 'appledatabase')

        sql= "select * from `register` where username= %s and password= %s"
        cursor = conn.cursor()
        cursor.execute(sql, (username,password))

        #check if there is a matching row
        if cursor.rowcount==0:
             return render_template('login.html',
                                    msg= 'Wrong Credentials')
        elif cursor.rowcount==1:
            from flask import redirect
            session ['username']= username
            # we need to protect / view with above session
            return redirect('/appointments')

        else:
            return render_template('login.html',
                                   msg= 'Error Encountered')

    else:
        return render_template('login.html')

#we route to view all appointments made
@app.route('/view')
def view():
    if 'username' in session:

        conn = pymysql.connect('localhost', 'root', '', 'appledatabase')
        sql= "select * from appointments"

        cursor =conn.cursor()
        cursor.execute(sql) #no values to pass

        #check how many rows cursor found
        if cursor.rowcount <=0:
            return render_template('view.html',
                                   msg= 'No appointments')
        #below returns rows back to the template
        else:
            rows= cursor.fetchall()
            return render_template('view.html',
                                   rows=rows)
    else:
        from flask import redirect
        return redirect('/login')




#logout route
#below route clears the session
@app.route('/logout')
def logout():
    session.pop ('username', None)
    from flask import redirect
    return redirect('/login')


#run the app
if __name__=='__main__':
        app.run(debug=True, port=2000)