from flask import Flask,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY']='HELLO WORLD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False

db=SQLAlchemy(app)

# data=[
#     {
#         'ipaddr':'192.168.1.13',
#         'dest_ip': '127.0.0.1',
#         'country':'INDIA'
#     },
#     {
#         'ipaddr': '192.168.1.12',
#         'dest_ip': '127.0.0.1',
#         'country':'USA'
#     }
# ]
class network_monitor(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ipaddr=db.Column(db.String(20),nullable=False)
    dest_ip = db.Column(db.String(120), nullable=False)
    country=db.Column(db.String(120), nullable=False)
    def __init__(self,ipaddr,dest_ip,country):
        self.ipaddr=ipaddr
        self.dest_ip=dest_ip
        self.country=country

db.create_all()

def add_data():
    n_data=network_monitor('192.168.1.20','127.0.0.1','India')
    db.session.add(n_data)
    db.session.commit()    
def get_data():
    data = network_monitor.query.all()
    return data
    
        

@app.route("/")
@app.route("/home")
def home():
    # add_data()
    # print('Data Added')
    return render_template('home.html')
@app.route("/dashboard")
def dashboard():
    count=network_monitor.query.count()
    chart_data=[0, 0, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
    
    return render_template('dashboard.html',data=get_data(),count=count,chart_data=chart_data)


@app.route("/team")
def team():
    return render_template('team.html') 

@app.route("/simple_chart")
def chart():
    legend = 'Countries'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)
@app.route("/article")
def article():
    return render_template('article.html') 

 

if __name__ == '__main__':
  app.run(debug=True)