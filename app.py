from flask import Flask, render_template, session, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from flask_mail import Mail, Message
import os
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm, ReportForm, ReturnForm
from models import db, Register, Report, Return

app = Flask(__name__)
app.config['SECRET_KEY'] = 'group9members'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:johnray08@localhost/LostLink'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'lostlink.official@gmail.com'
app.config['MAIL_PASSWORD'] = 'izhu jksj gqfs ilcj'
app.config['MAIL_DEFAULT_SENDER'] = 'lostlink.official@gmail.com'

mail = Mail(app)
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html', title = 'Lost Link')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)

        new_user = Register(
            sr_code = form.sr_code.data,
            name = form.name.data,
            surname = form.surname.data,
            age = form.age.data,
            email = form.email.data,
            contact = form.contact_number.data,
            gender = form.gender.data,
            username = form.username.data,
            password = hashed_password,
            role = form.role.data
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!")
        return redirect(url_for('login'))
    else:
        print(form.errors)

    return render_template('register.html', form=form, title = 'register')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Register.query.filter_by(sr_code = form.username.data).first()

        print(user)

        if user and check_password_hash(user.password, form.password.data):
            if not user.role:
                flash("User role not set. Contact admin.", "Danger")
                return redirect(url_for('login'))

            session['role'] = user.role
            session['sr_code'] = user.sr_code
            current_user = session['name'] = user.name
            
            role_lower = session['role'] = user.role

            if role_lower == 'student':
                return redirect(url_for('dashboard'))
            elif role_lower == 'admin':
                return redirect(url_for('admin', name=current_user))
        
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template('login.html', title = 'Login', form=form)

@app.route('/Logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html', title = 'about')

@app.route('/dashboard')
def dashboard():
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('dashboard.html', title = 'dashboard', reports=reports)


@app.route('/dashboard/Report', methods = ['GET', 'POST'])
def report():
    form = ReportForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)

        photo.save(os.path.join('static/uploads', filename))

        founder_sr_code = session.get('sr_code')

        new_report = Report (
            item = form.item.data,
            place = form.place.data,
            photo = filename,
            description = form.description.data,
            report_by = founder_sr_code
        )

        db.session.add(new_report)
        db.session.commit()

        flash("Report Submitted Successfully!")
        return redirect(url_for('dashboard'))
    
    return render_template('report.html', title = 'Report', form=form)


@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    current_admin = session.get('name')
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('admin.html', title = "Admin", name = current_admin, reports = reports)

@app.route('/admin/returning', methods = ['GET', 'POST'])
def returning():
    form = ReturnForm()

    if form.validate_on_submit():

        report_id = form.item_id.data
        report = Report.query.get(report_id)
        if not report:
            flash("Report not found!", "Danger")
            return redirect(url_for('admin'))
        
        returned_item = Return (
            item_id = report.id,
            item_name = report.item,
            place_found = report.place,
            photo = report.photo,
            description = report.description,
            claimed_by = form.name.data,
            email = form.email.data,
            contact = form.contact.data
        )

        db.session.add(returned_item)

        db.session.delete(report)

        db.session.commit()

        msg = Message (
            subject="LostLink: Item Claim Confirmation",
            recipients=[form.email.data]
        )

        msg.body = f"""
Hello {form.name.data},

Your claim for the item '{report.item}' has beed returned successfully.

Details:
- Item: {report.item}
- Place Found: {report.place}
- Description: {report.description}
- Contact Provided: {form.contact.data}

Thank you for using LostLink.


Regards,
LostLink Admin Team
"""
        mail.send(msg)

        flash("Claimed Successfully! Item moved to returned log.", "Success")
        return redirect(url_for('admin'))
    
    return render_template('returning.html', form=form, title='Return Items')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)