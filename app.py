from flask import Flask, render_template, session, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from flask_mail import Mail, Message
import os
from forms import LoginForm, RegisterForm, ReportForm, ReturnForm, UpdateForm
from models import db, Register, Report, Return

app = Flask(__name__)
app.config['SECRET_KEY'] = 'group9members'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:johnray08@localhost/LostLink'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'lostlink.official@gmail.com'
app.config['MAIL_PASSWORD'] = 'izhu jksj gqfs ilcj'
app.config['MAIL_DEFAULT_SENDER'] = 'lostlink.official@gmail.com'

mail = Mail(app)
db.init_app(app)

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'sr_code' not in session:
            flash('You must be logged in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html', title = 'Lost Link')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            # Check if sr_code already exists
            existing_sr = Register.query.filter_by(sr_code=form.sr_code.data).first()
            if existing_sr:
                flash("Sr-Code already registered!", "danger")
                return render_template('register.html', form=form, title='register')
            
            # Check if username already exists
            existing_user = Register.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash("Username already taken!", "danger")
                return render_template('register.html', form=form, title='register')

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
                role = "student"
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {str(e)}")
            flash(f"Registration error: {str(e)}", "danger")
    else:
        # Print form errors for debugging
        if form.errors:
            print(f"Form validation errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", "danger")
    
    return render_template('register.html', form=form, title='register')

@app.route('/register_admin', methods = ['GET', 'POST'])
def register_admin():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            # Check if sr_code already exists
            existing_sr = Register.query.filter_by(sr_code=form.sr_code.data).first()
            if existing_sr:
                flash("Sr-Code already registered!", "danger")
                return render_template('register.html', form=form, title='register')
            
            # Check if username already exists
            existing_user = Register.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash("Username already taken!", "danger")
                return render_template('register.html', form=form, title='register')

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
                role = "admin"
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {str(e)}")
            flash(f"Registration error: {str(e)}", "danger")
    else:
        # Print form errors for debugging
        if form.errors:
            print(f"Form validation errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", "danger")
    
    return render_template('register_admin.html', form=form, title='Admin Register')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Register.query.filter_by(sr_code = form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            if not user.role:
                flash("User role not set. Contact admin.", "danger")
                return redirect(url_for('login'))

            session['role'] = user.role
            session['sr_code'] = user.sr_code
            session['name'] = user.name

            if user.role == 'student':
                return redirect(url_for('dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin'))
        
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
@login_required
def dashboard():
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('dashboard.html', title = 'dashboard', reports=reports)


@app.route('/dashboard/Report', methods = ['GET', 'POST'])
@login_required
def report():
    form = ReportForm()
    # Only show reports created by the currently logged-in user
    current_sr_code = session.get('sr_code')
    reports = Report.query.filter_by(report_by=current_sr_code).order_by(Report.id.desc()).all()

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
    
    return render_template('report.html', title = 'Report', form=form, reports = reports, sr_code = current_sr_code)


@app.route('/admin', methods = ['GET', 'POST'])
@login_required
def admin():
    if session.get('role') != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    current_admin = session.get('name')
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('admin.html', title = "Admin", name = current_admin, reports = reports)

@app.route('/admin/returning', methods = ['GET', 'POST'])
@login_required
def returning():
    if session.get('role') != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    form = ReturnForm()
    current_admin = session.get('name')

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

Good day!

We are pleased to inform you that your claim has been successfully processed, and the item listed below has been returned.

------------------------------
ITEM DETAILS
------------------------------
Item Name       : {returned_item.item_name}
Place Found     : {returned_item.place_found}
Description     : {returned_item.description}
Contact Provided: {returned_item.contact}
------------------------------

If you have any questions or need further assistance, feel free to contact us.

Thank you for trusting LostLink in helping recover your belongings.

Best regards,

LostLink Admin Team
"""

        # HTML Email (Recommended)
        msg.html = f"""
<html>
<body>
    <p>Hello <strong>{form.name.data}</strong>,</p>

    <p>Good day!</p>

    <p>
        We are pleased to inform you that your claim has been 
        <strong>successfully processed</strong>. Below are the details of the returned item:
    </p>

    <hr>

    <h3>Item Details</h3>
    <ul>
        <li><strong>Item Name:</strong> {returned_item.item_name}</li>
        <li><strong>Place Found:</strong> {returned_item.place_found}</li>
        <li><strong>Description:</strong> {returned_item.description}</li>
        <li><strong>Contact Provided:</strong> {returned_item.contact}</li>
    </ul>

    <hr>

    <p>
        If you have any questions or need further assistance, feel free to reach out.
    </p>

    <p>
        Thank you for trusting <strong>LostLink</strong>.
    </p>

    <p>
        Best regards,<br>
        <strong>LostLink Admin Team</strong>
    </p>
</body>
</html>
"""
        mail.send(msg)

        flash("Claimed Successfully! Item moved to returned log.", "Success")
        return redirect(url_for('admin'))
    
    return render_template('returning.html', form=form, title='Return Items', name = current_admin)

@app.route('/update/<int:item_id>', methods = ['GET', 'POST'])
@login_required
def update_report(item_id):
    report = Report.query.get_or_404(item_id)
    form = UpdateForm()
    current_user = session.get('role')

    if request.method == 'POST':
        report.item = form.item.data or report.item
        report.place = form.place.data or report.place
        report.description = form.description.data or report.description
        db.session.commit()
        flash("Report updated successfully!", "success")

        if current_user == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('dashboard'))
    else:
        form.item.data = report.item
        form.place.data = report.place
        form.description.data = report.description
        
    if current_user == 'admin':
        return render_template('update_admin.html', report = report, form = form, title = 'Update Report')
    else:
        return render_template('update.html', report = report, form = form, title = 'Update Report')

@app.route('/delete/<int:item_id>', methods = ['POST'])
@login_required
def delete_report(item_id):
    report = Report.query.get_or_404(item_id)
    current_user = session.get('role')
    
    if current_user == 'admin' or report.report_by == session.get('sr_code'):
        db.session.delete(report)
        db.session.commit()
        flash("Report Deleted!", "info")
    else:
        flash("You don't have permission to delete this report.", "danger")
    
    if current_user == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/admin/returned', methods = ['GET', 'POST'])
@login_required
def returned():
    if session.get('role') != 'admin':
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    current_admin = session.get('name')
    returned = Return.query.order_by(Return.id.asc()).all()
    return render_template('returned.html', title = "Returned Items", returned = returned, name = current_admin)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)