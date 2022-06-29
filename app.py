from flask import Flask, render_template, request, redirect
import boto3
import datetime
from time import strftime
import pytz
import config
import os

app = Flask(__name__)

os.environ['AWS_ACCESS_KEY_ID '] = config.AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = config.AWS_SECRET_ACCESS_KEY
os.environ['REGION_NAME']= "us-west-2"

session = boto3.Session(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name= "us-west-2"
)

dynamodb = session.resource(
        'dynamodb')

@app.route('/', methods = ['POST','GET'])
def feedback():
    
    if 'satisfaction' in request.form and 'suggestions' in request.form:
        satisfaction = request.form.get('satisfaction')
        suggestions = request.form.get('suggestions')
        ip = request.environ['REMOTE_ADDR']
        date_object = str(datetime.date.today())
        ist = pytz.timezone('Asia/Kolkata')
        time_object = str(strftime("%H:%M:%S"))

        feedback_table = dynamodb.Table('feedback_table')

        feedback_table.put_item(Item={
            'satisfaction':satisfaction,
            'suggestions':suggestions,
            'ip_address':ip,
            'date': date_object,
            'timestamp': time_object,
         })

        return redirect('/thanks')
    
    return render_template("home.html")

@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

@app.route('/duplicate')
def duplicate():
    return render_template("duplicate.html")

if __name__ == '__main__':
    app.debug = True
    app.run()

