import random
import sys

try:
    from app import create_app
    from app.extensions import db
    from app.models import Admin, Department, Internship
except ModuleNotFoundError as e:
    missing = str(e).split()[-1].strip("'\n")
    print(f"❌ Missing dependency: {missing}")
    print()
    print("To fix this, activate your environment and install dependencies:")
    print()
    print("    .\\venv\\Scripts\\Activate.ps1")
    print("    pip install -r requirements.txt")
    print()
    print("Then run:")
    print("    python seed.py")
    sys.exit(1)


# Initialize app
app = create_app()
app.app_context().push()

print("Using DB:", app.config["SQLALCHEMY_DATABASE_URI"])


# --------- SEED ADMIN ---------
admin = Admin.query.first()
if not admin:
    admin = Admin(
        email="admin@internship.gov.in",
        name="System Administrator"
    )
    admin.set_password("Admin@123")
    db.session.add(admin)
    db.session.commit()

    print("\n🟢 Admin created successfully:")
    print(f"   Email: admin@internship.gov.in")
    print(f"   Password: Admin@123")
else:
    print("\nℹ️ Admin already exists:")
    print(f"   Email: {admin.email}")


# --------- SEED DEPARTMENTS ---------
departments = [
    {
        "name": "National e-Governance Division",
        "email": "negd@meity.gov.in",
        "password": "Negd@123",
        "ministry": "Ministry of Electronics and IT",
        "department_type": "Central",
        "location": "New Delhi, Delhi",
        "contact_person": "Rakesh Sharma",
        "contact_phone": "9876543210",
        "description": "Works on implementing Digital India initiatives."
    },
    {
        "name": "Department of Higher Education",
        "email": "dhe@mhrd.gov.in",
        "password": "Edu@123",
        "ministry": "Ministry of Education",
        "department_type": "Central",
        "location": "New Delhi, Delhi",
        "contact_person": "Anjali Verma",
        "contact_phone": "9876501234",
        "description": "Handles policy-making and research in higher education."
    },
    {
        "name": "Department of Health Research",
        "email": "dhr@mohfw.gov.in",
        "password": "Health@123",
        "ministry": "Ministry of Health and Family Welfare",
        "department_type": "Central",
        "location": "Pune, Maharashtra",
        "contact_person": "Dr. Vivek Joshi",
        "contact_phone": "9811122233",
        "description": "Promotes and funds health research in medical institutions."
    },
    {
        "name": "Department of Renewable Energy",
        "email": "dre@mnre.gov.in",
        "password": "Green@123",
        "ministry": "MoRNE",
        "department_type": "Central",
        "location": "Bengaluru, Karnataka",
        "contact_person": "Priya Nair",
        "contact_phone": "9823345567",
        "description": "Develops policies for solar, wind, and renewable energy."
    }
]

seeded_departments = []

for data in departments:
    existing = Department.query.filter_by(email=data["email"]).first()

    if not existing:
        dept = Department(
            name=data["name"],
            email=data["email"],
            ministry=data["ministry"],
            department_type=data["department_type"],
            location=data["location"],
            contact_person=data["contact_person"],
            contact_phone=data["contact_phone"],
            description=data["description"],
            created_by=admin.id
        )
        dept.set_password(data["password"])
        db.session.add(dept)
        seeded_departments.append(dept)

db.session.commit()
print(f"\n🟢 {len(seeded_departments)} departments seeded successfully!")


# --------- SEED INTERNSHIPS ---------
titles = [
    "Research Intern", "Policy Analyst Intern", "Software Developer Intern",
    "AI Research Intern", "Data Science Intern", "Cybersecurity Intern"
]

skills = [
    "Python, SQL, Data Analysis",
    "Research, Writing, Communication",
    "Machine Learning, TensorFlow",
    "Cloud Computing, AWS"
]

courses = [
    "Computer Science", "Economics", "Public Policy",
    "Environmental Science", "Civil Engineering"
]

locations = [
    "New Delhi", "Mumbai", "Bengaluru", "Chennai", "Pune"
]

total_created = 0

for dept in Department.query.all():
    for i in range(10):
        internship = Internship(
            company_id=dept.id,
            title=f"{random.choice(titles)} #{i+1}",
            description=f"{dept.name} internship role.",
            sector=random.choice(["Technology", "Policy", "Energy", "Environment"]),
            location=random.choice(locations),
            required_skills=random.choice(skills),
            preferred_course=random.choice(courses),
            min_cgpa=round(random.uniform(6.0, 9.0), 2),
            year_of_study_requirement=random.choice(["2nd Year", "3rd Year", "Final Year"]),
            total_positions=random.randint(2, 10),
            duration_months=random.randint(2, 6),
            stipend=random.choice([5000, 8000, 10000, 12000])
        )

        db.session.add(internship)
        total_created += 1

db.session.commit()

print(f"🟢 {total_created} internships seeded successfully!")
print("\n🎉 Database seeding completed!")
