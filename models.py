from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

class Retreat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)  
    date = db.Column(db.Integer)  
    location = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(128)) 
    condition = db.Column(db.String(128))  
    image = db.Column(db.String(2048)) 
    duration  =  db.Column(db.Integer) 

    def __repr__(self):
        return f"<Retreat {self.title}>"  



class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    user_phone = db.Column(db.String(20), nullable=False)
    retreat_id = db.Column(db.Integer, db.ForeignKey('retreat.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    payment_type = db.Column(db.String(10), nullable=False)
    payment_screenshot = db.Column(db.String(255)) 


