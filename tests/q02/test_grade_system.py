# test_grade_system.py

import pytest
from datetime import datetime, timedelta
from grade_system import GradeManager, GradeLevel

@pytest.fixture
def grade_manager():
    return GradeManager()

@pytest.fixture
def setup_course(grade_manager):
    course = grade_manager.add_course("Math 101")
    grade_manager.enroll_student("S1", "John Doe", "Math 101")
    grade_manager.enroll_student("S2", "Jane Smith", "Math 101")
    return course

def test_course_enrollment(grade_manager, setup_course):
    assert "S1" in setup_course.enrolled_students
    assert "S2" in setup_course.enrolled_students
    assert len(setup_course.enrolled_students) == 2
    assert grade_manager.student_names["S1"] == "John Doe"

def test_assignment_grading(grade_manager, setup_course):
    due_date = datetime.now() + timedelta(days=7)
    assignment = setup_course.add_assignment("Homework 1", 0.5, due_date)
    
    grade_manager.record_grade("Math 101", "Homework 1", "S1", 85.0)
    grade_manager.record_grade("Math 101", "Homework 1", "S2", 92.0)
    
    assert assignment.grades["S1"] == 85.0
    assert assignment.grades["S2"] == 92.0

def test_student_average(grade_manager, setup_course):
    due_date = datetime.now() + timedelta(days=7)
    setup_course.add_assignment("Homework 1", 0.5, due_date)
    setup_course.add_assignment("Test 1", 0.5, due_date)
    
    grade_manager.record_grade("Math 101", "Homework 1", "S1", 80.0)
    grade_manager.record_grade("Math 101", "Test 1", "S1", 90.0)
    
    average = grade_manager.get_student_average("Math 101", "S1")
    assert average == 85.0

def test_course_average(grade_manager, setup_course):
    due_date = datetime.now() + timedelta(days=7)
    setup_course.add_assignment("Homework 1", 1.0, due_date)
    
    grade_manager.record_grade("Math 101", "Homework 1", "S1", 80.0)
    grade_manager.record_grade("Math 101", "Homework 1", "S2", 90.0)
    
    average = grade_manager.get_course_average("Math 101")
    assert average == 85.0

def test_letter_grade(grade_manager):
    assert grade_manager.get_letter_grade(95.0) == GradeLevel.A
    assert grade_manager.get_letter_grade(85.0) == GradeLevel.B
    assert grade_manager.get_letter_grade(75.0) == GradeLevel.C
    assert grade_manager.get_letter_grade(65.0) == GradeLevel.D
    assert grade_manager.get_letter_grade(55.0) == GradeLevel.F

def test_academic_alerts(grade_manager, setup_course):
    due_date = datetime.now() + timedelta(days=7)
    setup_course.add_assignment("Test 1", 1.0, due_date)
    
    grade_manager.record_grade("Math 101", "Test 1", "S1", 55.0)
    assert "Math 101" in grade_manager.academic_alerts["S1"]
    
    grade_manager.record_grade("Math 101", "Test 1", "S1", 75.0)
    assert "S1" not in grade_manager.academic_alerts

def test_missing_assignments(grade_manager, setup_course):
    past_date = datetime.now() - timedelta(days=1)
    future_date = datetime.now() + timedelta(days=7)
    
    setup_course.add_assignment("Past Assignment", 1.0, past_date)
    setup_course.add_assignment("Future Assignment", 1.0, future_date)
    
    missing = grade_manager.get_missing_assignments("Math 101", "S1")
    assert "Past Assignment" in missing
    assert "Future Assignment" not in missing