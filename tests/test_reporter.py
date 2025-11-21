import pytest
import tempfile
import os
from src.reporter import ReportGenerator

@pytest.fixture
def sample_csv_files():
    files = []
    data1 = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,Python, Django, PostgreSQL, Docker,API Team,5
Maria Petrova,Frontend Developer,38,4.7,React, TypeScript, Redux, CSS,Web Team,4"""

    data2 = """name,position,completed_tasks,performance,skills,team,experience_years
John Smith,Data Scientist,29,4.6,Python, ML, SQL, Pandas,AI Team,3
Anna Lee,DevOps Engineer,52,4.9,AWS, Kubernetes, Terraform, Ansible,Infrastructure Team,6"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f1:
        f1.write(data1)
        files.append(f1.name)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f2:
        f2.write(data2)
        files.append(f2.name)

    yield files

    for f in files:
        os.unlink(f)

def test_load_files(sample_csv_files):
    gen = ReportGenerator()
    gen.load_files(sample_csv_files)
    assert len(gen.data) == 4  

def test_generate_performance_report(sample_csv_files):
    gen = ReportGenerator()
    gen.load_files(sample_csv_files)
    report = gen.generate_performance_report()
    
    positions = [r['position'] for r in report]
    assert "Backend Developer" in positions
    assert "Frontend Developer" in positions
    assert "Data Scientist" in positions
    assert "DevOps Engineer" in positions

    performances = [r['average_performance'] for r in report]
    assert performances == sorted(performances, reverse=True)

def test_file_not_found():
    gen = ReportGenerator()
    with pytest.raises(FileNotFoundError):
        gen.load_files(["nonexistent.csv"])

def test_invalid_performance_value():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("""name,position,completed_tasks,performance,skills,team,experience_years
Invalid User,Tester,10,not_a_number,Some Skill,Team,2""")
        file_path = f.name

    gen = ReportGenerator()
    with pytest.raises(ValueError):
        gen.load_files([file_path])

    os.unlink(file_path)