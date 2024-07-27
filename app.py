from flask import Flask, render_template, request, redirect, url_for, abort
from models import Retreat, db, Booking
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:revathyarjun@localhost:5432/retreat_database'

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/retreats')
def retreats():
    retreats = Retreat.query.all()
    return render_template('retreatpage.html', retreats=retreats)



@app.route('/search', methods=['GET', 'POST'])
def search():
  if request.method == 'POST':
      search_query = request.form['search']
      results = Retreat.query.filter(Retreat.condition.ilike(f'%{search_query}%') | Retreat.location.ilike(f'%{search_query}%')).all()
  return render_template('resultpage.html',results=results)
    

@app.route('/book_retreat/<int:retreat_id>')
def book_retreat(retreat_id):
    retreat = Retreat.query.get(retreat_id)
    if retreat is None:
        return abort(404)
    return render_template('booking_form.html', retreat=retreat)

@app.route('/book', methods=['POST'])
def booking():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_email = request.form['user_email']
    user_phone = request.form['user_phone']
    retreat_id = request.form['retreat_id']
    booking_date = request.form['booking_date']
    payment_type = request.form['payment_type']
    payment_screenshot = request.files['payment_screenshot'] if 'payment_screenshot' in request.files else None


    existing_booking = Booking.query.filter_by(user_id=user_id, retreat_id=retreat_id, booking_date=booking_date).first()
    if existing_booking:
        return render_template('booking_error.html')

    booking = Booking(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        retreat_id=retreat_id,
        booking_date=booking_date,
        payment_type=payment_type,
    )

    
    if payment_screenshot:
        
        

        upload_folder = 'uploads/payment_screenshots'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = secure_filename(payment_screenshot.filename)
        filepath = os.path.join(upload_folder, filename)

        payment_screenshot.save(filepath)
        booking.payment_screenshot_path = filepath

    try:
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('booking_confirmation'))
    except Exception as e:
        return render_template('error.html', error_message=str(e))

@app.route('/booking_confirmation')
def booking_confirmation():
    return render_template('booking_confirmation.html')



if __name__ == '__main__':
    app.run(debug=True)
