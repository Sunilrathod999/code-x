import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app import app, db
from models import Admin, Content, Service, ContactMessage, SiteSettings
from datetime import datetime


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_site_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    return settings


def get_content(section):
    content = Content.query.filter_by(section=section).first()
    if not content:
        default_content = {
            'home': "We specialize in <span class='fw-bold text-success'>professional</span> <span class='fw-bold text-primary'>furniture</span> <span class='fw-bold text-warning'>installation</span> services for homes and offices, including <span class='fw-bold text-info'>modular furniture</span>, <span class='fw-bold text-danger'>workstations</span>, <span class='fw-bold text-success'>kitchen units</span>, and more. Our experienced technicians ensure <span class='fw-bold text-primary'>precise</span>, <span class='fw-bold text-success'>safe</span>, and <span class='fw-bold text-warning'>fast</span> installations using <span class='fw-bold text-info'>advanced tools</span>, helping you enjoy your space without hassle, all at <span class='fw-bold text-dark'>affordable</span> prices.",
            'about': "At MTS Furnitech, we are dedicated to providing <span class='fw-bold text-success'>professional</span> furniture installation services that transform your space efficiently and affordably. Our experienced team specializes in both office and home furniture installations, ensuring every piece is assembled with precision and care. We understand that your time is valuable, which is why we focus on <span class='fw-bold text-primary'>fast</span>, reliable service without compromising on quality. From modular workstations to custom kitchen units, we handle every installation with the expertise and attention to detail that your furniture deserves."
        }
        content = Content(section=section, content=default_content.get(section, ''))
        db.session.add(content)
        db.session.commit()
    return content


def init_default_services():
    if Service.query.count() == 0:
        office_services = [
            "Modular Furniture Installation",
            "Executive Office Desk Installation", 
            "Reception Desk Installation",
            "Modular Conference Table Installation",
            "Modular Cabin Table Installation",
            "Wardrobe Installation",
            "Cabinet Installation",
            "Office Workstation Installation"
        ]
        
        home_services = [
            "Bed Installation",
            "Bedroom Wardrobe Installation",
            "TV Unit Installation",
            "Modular Kitchen Installation"
        ]
        
        for i, service in enumerate(office_services):
            s = Service(
                title=service,
                description=f"Professional {service.lower()} service with experienced technicians and quality tools.",
                category='office',
                order_index=i
            )
            db.session.add(s)
        
        for i, service in enumerate(home_services):
            s = Service(
                title=service,
                description=f"Expert {service.lower()} service for your home with precision and care.",
                category='home',
                order_index=i
            )
            db.session.add(s)
        
        db.session.commit()


@app.route('/')
def index():
    settings = get_site_settings()
    content = get_content('home')
    return render_template('index.html', settings=settings, content=content)


@app.route('/services')
def services():
    settings = get_site_settings()
    init_default_services()
    
    office_services = Service.query.filter_by(category='office', is_active=True).order_by(Service.order_index).all()
    home_services = Service.query.filter_by(category='home', is_active=True).order_by(Service.order_index).all()
    
    return render_template('services.html', 
                         settings=settings, 
                         office_services=office_services, 
                         home_services=home_services)


@app.route('/about')
def about():
    settings = get_site_settings()
    content = get_content('about')
    return render_template('about.html', settings=settings, content=content)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = get_site_settings()
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        service_interest = request.form.get('service_interest')
        message = request.form.get('message')
        
        if name and phone and service_interest and message:
            contact_msg = ContactMessage(
                name=name,
                phone=phone,
                service_interest=service_interest,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            flash('Your message has been sent successfully! We will contact you soon.', 'success')
            return redirect(url_for('contact'))
        else:
            flash('Please fill in all fields.', 'error')
    
    return render_template('contact.html', settings=settings)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))


def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/admin')
@admin_required
def admin_dashboard():
    settings = get_site_settings()
    message_count = ContactMessage.query.count()
    unread_count = ContactMessage.query.filter_by(is_read=False).count()
    service_count = Service.query.count()
    
    return render_template('admin/dashboard.html', 
                         settings=settings,
                         message_count=message_count,
                         unread_count=unread_count,
                         service_count=service_count)


@app.route('/admin/content', methods=['GET', 'POST'])
@admin_required
def admin_content():
    settings = get_site_settings()
    
    if request.method == 'POST':
        section = request.form.get('section')
        content_text = request.form.get('content')
        
        if section and content_text:
            content = Content.query.filter_by(section=section).first()
            if content:
                content.content = content_text
                content.updated_at = datetime.utcnow()
            else:
                content = Content(section=section, content=content_text)
                db.session.add(content)
            
            db.session.commit()
            flash(f'{section.title()} content updated successfully!', 'success')
        
        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(file_path)
                
                settings.logo_path = f'uploads/{filename}'
                db.session.commit()
                flash('Logo updated successfully!', 'success')
        
        # Handle contact information updates
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        whatsapp_number = request.form.get('whatsapp_number')
        address = request.form.get('address')
        
        if phone_number:
            settings.phone_number = phone_number
        if email:
            settings.email = email
        if whatsapp_number:
            settings.whatsapp_number = whatsapp_number
        if address:
            settings.address = address
            
        if phone_number or email or whatsapp_number or address:
            db.session.commit()
            flash('Contact information updated successfully!', 'success')
    
    home_content = get_content('home')
    about_content = get_content('about')
    
    return render_template('admin/edit_content.html', 
                         settings=settings,
                         home_content=home_content,
                         about_content=about_content)


@app.route('/admin/services', methods=['GET', 'POST'])
@admin_required
def admin_services():
    settings = get_site_settings()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            title = request.form.get('title')
            description = request.form.get('description')
            category = request.form.get('category')
            
            if title and description and category:
                service = Service(
                    title=title,
                    description=description,
                    category=category,
                    order_index=Service.query.filter_by(category=category).count()
                )
                
                # Handle image upload
                if 'image' in request.files:
                    file = request.files['image']
                    print(f"DEBUG ADD: File received: {file.filename if file else 'None'}")
                    print(f"DEBUG ADD: File size: {len(file.read()) if file else 0} bytes")
                    file.seek(0)  # Reset file pointer after reading
                    
                    if file and file.filename and file.filename.strip() != '':
                        print(f"DEBUG ADD: Checking file extension for: {file.filename}")
                        if allowed_file(file.filename):
                            # Check file size for better performance
                            file_size = len(file.read())
                            file.seek(0)  # Reset file pointer
                            
                            if file_size > 5 * 1024 * 1024:  # 5MB limit
                                flash('File too large. Maximum size is 5MB.', 'error')
                            else:
                                filename = secure_filename(file.filename)
                                # Add timestamp to filename to avoid conflicts
                                timestamp = str(int(datetime.now().timestamp()))
                                name, ext = os.path.splitext(filename)
                                filename = f"{name}_{timestamp}{ext}"
                                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                                
                                # Ensure upload directory exists
                                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                                print(f"DEBUG ADD: Saving file to: {file_path}")
                                
                                try:
                                    file.save(file_path)
                                    service.image_path = f'uploads/{filename}'
                                    print(f"DEBUG ADD: Image path set to: {service.image_path}")
                                    print(f"DEBUG ADD: File saved successfully")
                                except Exception as e:
                                    print(f"DEBUG ADD: Error saving file: {str(e)}")
                                    flash(f'Error uploading image: {str(e)}', 'error')
                        else:
                            print(f"DEBUG ADD: File not allowed: {file.filename}")
                            flash('File type not allowed. Please use JPG, PNG, GIF, SVG, or WebP images.', 'error')
                    else:
                        print("DEBUG ADD: No file selected or empty filename")
                
                db.session.add(service)
                db.session.commit()
                flash('Service added successfully!', 'success')
                return redirect(url_for('admin_services'))
        
        elif action == 'edit':
            service_id = request.form.get('service_id')
            service = Service.query.get_or_404(service_id)
            
            service.title = request.form.get('title')
            service.description = request.form.get('description')
            service.category = request.form.get('category')
            
            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                print(f"DEBUG EDIT: File received: {file.filename if file else 'None'}")
                print(f"DEBUG EDIT: File size: {len(file.read()) if file else 0} bytes")
                file.seek(0)  # Reset file pointer after reading
                
                if file and file.filename and file.filename.strip() != '':
                    print(f"DEBUG EDIT: Checking file extension for: {file.filename}")
                    if allowed_file(file.filename):
                        # Check file size for better performance
                        file_size = len(file.read())
                        file.seek(0)  # Reset file pointer
                        
                        if file_size > 5 * 1024 * 1024:  # 5MB limit
                            flash('File too large. Maximum size is 5MB.', 'error')
                        else:
                            filename = secure_filename(file.filename)
                            # Add timestamp to filename to avoid conflicts
                            timestamp = str(int(datetime.now().timestamp()))
                            name, ext = os.path.splitext(filename)
                            filename = f"{name}_{timestamp}{ext}"
                            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                            
                            # Ensure upload directory exists
                            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                            print(f"DEBUG EDIT: Saving file to: {file_path}")
                            
                            try:
                                file.save(file_path)
                                service.image_path = f'uploads/{filename}'
                                print(f"DEBUG EDIT: Image path set to: {service.image_path}")
                                print(f"DEBUG EDIT: File saved successfully")
                            except Exception as e:
                                print(f"DEBUG EDIT: Error saving file: {str(e)}")
                                flash(f'Error uploading image: {str(e)}', 'error')
                    else:
                        print(f"DEBUG EDIT: File not allowed: {file.filename}")
                        flash('File type not allowed. Please use JPG, PNG, GIF, SVG, or WebP images.', 'error')
                else:
                    print("DEBUG EDIT: No file selected or empty filename")
            
            db.session.commit()
            flash('Service updated successfully!', 'success')
            return redirect(url_for('admin_services'))
        
        elif action == 'delete':
            service_id = request.form.get('service_id')
            service = Service.query.get_or_404(service_id)
            db.session.delete(service)
            db.session.commit()
            flash('Service deleted successfully!', 'success')
            return redirect(url_for('admin_services'))
    
    services = Service.query.order_by(Service.category, Service.order_index).all()
    return render_template('admin/manage_services.html', settings=settings, services=services)


@app.route('/admin/change-password', methods=['GET', 'POST'])
@admin_required
def admin_change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Get current admin
        admin = Admin.query.filter_by(username=session.get('admin_username')).first()
        if not admin:
            flash('Session expired. Please login again.', 'error')
            return redirect(url_for('admin_login'))
        
        # Validate current password
        if not check_password_hash(admin.password_hash, current_password):
            flash('Current password is incorrect!', 'error')
            return render_template('admin/change_password.html')
        
        # Validate new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match!', 'error')
            return render_template('admin/change_password.html')
        
        # Validate password length
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('admin/change_password.html')
        
        # Update password
        admin.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/change_password.html')


@app.route('/admin/messages')
@admin_required
def admin_messages():
    settings = get_site_settings()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', settings=settings, messages=messages)


@app.route('/admin/message/<int:message_id>/read', methods=['POST'])
@admin_required
def mark_message_read(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()
    return redirect(url_for('admin_messages'))


@app.route('/admin/message/<int:message_id>/delete', methods=['POST'])
@admin_required
def delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin_messages'))
