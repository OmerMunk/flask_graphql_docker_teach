# load_data.py

import csv
from models import UserModel, SubjectModel
from database import db_session, init_db
from datetime import datetime

def load_data():
    init_db()

    # Load subjects
    with open('subjects.csv', 'r') as f:
        reader = csv.DictReader(f)
        subjects = {}
        for row in reader:
            subject = SubjectModel(name=row['name'])
            db_session.add(subject)
            db_session.commit()
            subjects[subject.name] = subject

    # Load users and their subjects
    with open('users.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            birth_date = datetime.strptime(row['birth_date'], '%Y-%m-%d').date()
            user = UserModel(
                name=row['name'],
                birth_date=birth_date
            )
            # Add subjects to user
            subject_names = row['subjects'].split(';')
            for name in subject_names:
                name = name.strip()
                subject = subjects.get(name)
                if subject:
                    user.subjects.append(subject)
            db_session.add(user)
        db_session.commit()

if __name__ == '__main__':
    load_data()
