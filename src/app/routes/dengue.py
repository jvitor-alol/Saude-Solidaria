from flask import Blueprint, render_template

dengue_bp = Blueprint('dengue', __name__, template_folder='../templates')

@dengue_bp.route('/dengue')
def dengue_info():
    return render_template('dengue.html')
