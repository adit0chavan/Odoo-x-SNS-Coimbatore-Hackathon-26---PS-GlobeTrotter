from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/')
@login_required
def view():
    return render_template('profile/view.html')

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.bio = request.form.get('bio')
        current_user.language = request.form.get('language', 'en')
        
        # In a real app, we'd handle file upload for profile_pic here
        # For now, we'll allow a URL input for simplicity
        profile_pic_url = request.form.get('profile_pic_url')
        if profile_pic_url:
            current_user.profile_pic = profile_pic_url
            
        db.session.commit()
        flash('Profile successfully updated!', 'success')
        return redirect(url_for('profile.view'))
        
    return render_template('profile/edit.html')
