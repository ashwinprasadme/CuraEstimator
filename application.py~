#!flask/bin/python
import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, send_from_directory,render_template, jsonify
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
from settings import APP_STATIC,APP_UPLOAD,APP_SLIC3R,APP_ROOT
from subprocess import call, Popen
import gcoder
import rounder
import estimator
import send_email

UPLOAD_FOLDER = APP_UPLOAD
ALLOWED_EXTENSIONS = set(['stl', 'obj','STL','OBJ'])

application = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ab:iP@localhost/sales"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config.from_pyfile(settings.py)
db = SQLAlchemy(application)
#from app import app

class Order(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone_no = db.Column(db.String(15))
    filename = db.Column(db.String(120))
    pub_date = db.Column(db.DateTime)
    quality = db.Column(db.String(6))
    support = db.Column(db.String(5))


    def __init__(self, name, email, filename, phone_no, quality, support):
        self.name = name
        self.email = email
        self.filename = filename
        self.phone_no = phone_no
        self.quality = quality
        self.support = support
        self.pub_date = datetime.now()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@application.route('/test', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_no = request.form['phone_no']
        # file = request.files['file']
        file = request.files.getlist("file")
        # print file
        quality = request.form['quality']
        # speed = request.form['speed']
        support = "0"
        # if support == 'Yes':
        #     support == 1
        # else:
        #     support == 0

        filestls = []
        for fstl in file:
            filestls.append(fstl.filename)
        filelist = '[%s]' % ', '.join(map(str, filestls))

        order_db = Order(name, email , filelist, phone_no, quality, support)
        db.session.add(order_db)
        db.session.flush()
        order_id = order_db.id
        print order_id
        db.session.commit()

        # merging ORDER form
        print "\n"
        for files in file:
            if files and allowed_file(files.filename):
                filename = secure_filename(files.filename)
                print filename
                files.save(os.path.join(UPLOAD_FOLDER, filename))

                # Database entry
                # name, email, filename, phone_no, quality, speed, support


                Schedule_Processing = [os.path.join(APP_ROOT, "./estimator.py"), name, email, filename, quality, support,str(order_id)]
                print Schedule_Processing

                #Popen Estimator!
                Popen(Schedule_Processing)
        send_email.send_ACK(email,name,order_id) #Acknowledgement Mail
        return render_template('thanks.html',name=name,email=email)
    return render_template('temp.html')

@application.route('/dev', methods=['GET', 'POST'])
def dev():
    print "yes\n"
    if request.method == 'GET':
        quality = request.args.get('quality')
        print quality
        file = request.args.get('filename')
        print file
        print "here\n\n"
        Schedule_Processing = [os.path.join(APP_ROOT, "./estimator.py"),file, quality]
        print Schedule_Processing

        #Popen Estimator!
        Popen(Schedule_Processing)

    return "OK"

@application.route('/AdminEz3', methods=['GET', 'POST'])
def all():
    if request.method == 'POST':
        name = request.form['user']
        passw = request.form['password']
        if name == 'Admin' and passw == 'Ez3' :
            return render_template('list.html',todos=Order.query.order_by(Order.pub_date.desc()).all())
        else:
            return redirect('/AdminEz3')
    else:
        return render_template('EZAdmin.html')

@application.route('/', methods=['GET', 'POST'])
def gcodews():
    if request.method == 'POST':
        # email = request.form['email']
        # quality = request.form['quality']
        # print quality
        # file = request.files['file']
        print "here\n\n"
        file = request.files.getlist("files")
        print file
        for files in file:
            if files:
                filename = secure_filename(files.filename)
                stl_name = os.path.splitext(filename)[0] + ".stl"
                files.save(os.path.join(UPLOAD_FOLDER, stl_name))
                Schedule_Processing = [os.path.join(APP_ROOT, "./estimator.py"),stl_name]
                print Schedule_Processing
                #Popen Estimator!
                Popen(Schedule_Processing)
            return redirect('http://**.rhcloud.com/costofmodel?stlname='+ os.path.splitext(stl_name)[0])
    return render_template('cost.html')

@application.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
