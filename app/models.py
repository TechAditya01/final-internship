from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)  # Optional for Google auth
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))

    # Academic Information
    institution = db.Column(db.String(200))
    course = db.Column(db.String(100))
    year_of_study = db.Column(db.Integer)
    cgpa = db.Column(db.Float)

    # Skills and Interests
    technical_skills = db.Column(db.Text)
    soft_skills = db.Column(db.Text)
    sector_interests = db.Column(db.Text)

    # Location
    preferred_locations = db.Column(db.Text)
    current_location = db.Column(db.String(100))

    # Affirmative Action
    social_category = db.Column(db.String(50))
    district_type = db.Column(db.String(50))
    home_district = db.Column(db.String(100))

    # Participation
    previous_internships = db.Column(db.Integer, default=0)
    pm_scheme_participant = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    matches = db.relationship('Match', backref='student', lazy=True)
    applications = db.relationship('Application', backref='student', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return self.password_hash and check_password_hash(self.password_hash, password)

    def calculate_profile_completeness(self):
        fields = {
            'name': 10, 'email': 10, 'phone': 10, 'institution': 10, 'course': 10,
            'year_of_study': 5, 'cgpa': 5, 'technical_skills': 10, 'soft_skills': 5,
            'sector_interests': 10, 'current_location': 5, 'preferred_locations': 5,
            'social_category': 3, 'district_type': 3, 'home_district': 4,
            'previous_internships': 5, 'pm_scheme_participant': 5,
        }

        labels = {
            'name': 'Full Name', 'email': 'Email', 'phone': 'Phone Number', 'institution': 'Institution',
            'course': 'Course/Degree', 'year_of_study': 'Year of Study', 'cgpa': 'CGPA/Percentage',
            'technical_skills': 'Technical Skills', 'soft_skills': 'Soft Skills',
            'sector_interests': 'Sector Interests', 'current_location': 'Current Location',
            'preferred_locations': 'Preferred Locations', 'social_category': 'Social Category',
            'district_type': 'District Type', 'home_district': 'Home District',
            'previous_internships': 'Number of Previous Internships',
            'pm_scheme_participant': 'PM Scheme Participant',
        }

        score = 0
        missing = []

        for field, weight in fields.items():
            value = getattr(self, field)
            if value is not None and value != "":
                score += weight
            else:
                missing.append(labels[field])

        return min(score, 100), missing


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(200), nullable=False)

    ministry = db.Column(db.String(200))
    department_type = db.Column(db.String(100))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)

    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(15))

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)

    internships = db.relationship('Internship', backref='department', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(50), default='admin')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    created_departments = db.relationship('Department', backref='admin_creator', lazy=True)


class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sector = db.Column(db.String(100))
    location = db.Column(db.String(100))

    required_skills = db.Column(db.Text)
    preferred_course = db.Column(db.String(100))
    min_cgpa = db.Column(db.Float)
    year_of_study_requirement = db.Column(db.String(50))

    total_positions = db.Column(db.Integer, default=1)
    filled_positions = db.Column(db.Integer, default=0)
    duration_months = db.Column(db.Integer)
    stipend = db.Column(db.Float)

    rural_quota = db.Column(db.Integer, default=0)
    sc_quota = db.Column(db.Integer, default=0)
    st_quota = db.Column(db.Integer, default=0)
    obc_quota = db.Column(db.Integer, default=0)

    is_active = db.Column(db.Boolean, default=True)
    application_deadline = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    matches = db.relationship('Match', backref='internship', lazy=True)
    applications = db.relationship('Application', backref='internship', lazy=True)


class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'), nullable=False)

    overall_score = db.Column(db.Float, nullable=False)
    skills_score = db.Column(db.Float)
    location_score = db.Column(db.Float)
    academic_score = db.Column(db.Float)
    affirmative_action_score = db.Column(db.Float)

    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('student_id', 'internship_id'),)


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'), nullable=False)

    cover_letter = db.Column(db.Text)
    portfolio_url = db.Column(db.String(255))
    additional_notes = db.Column(db.Text)

    status = db.Column(db.String(50), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department_notes = db.Column(db.Text)
    interview_date = db.Column(db.DateTime)
    response_date = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint('student_id', 'internship_id'),)
