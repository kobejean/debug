# grade_system.py

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional

class GradeLevel(Enum):
    A = 4.0
    B = 3.0
    C = 2.0
    D = 1.0
    F = 0.0

class Assignment:
    def __init__(self, name: str, weight: float, due_date: datetime):
        self.name = name
        self.weight = weight
        self.due_date = due_date
        self.grades: Dict[str, float] = {}
        
    def add_grade(self, student_id: str, score: float) -> None:
        if score > 100:
            score = 100
        self.grades[student_id] = score

class Course:
    def __init__(self, name: str, min_passing_grade: float = 60.0):
        self.name = name
        self.assignments: List[Assignment] = []
        self.min_passing_grade = min_passing_grade
        self.enrolled_students: List[str] = []
        
    def enroll_student(self, student_id: str) -> None:
        if student_id in self.enrolled_students:
            return
        self.enrolled_students.append(student_id)
        
    def add_assignment(self, name: str, weight: float, due_date: datetime) -> Assignment:
        assignment = Assignment(name, weight, due_date)
        self.assignments.append(assignment)
        return assignment

class GradeManager:
    def __init__(self):
        self.courses: Dict[str, Course] = {}
        self.student_names: Dict[str, str] = {}
        self.academic_alerts: Dict[str, List[str]] = {}
        
    def add_course(self, name: str) -> Course:
        course = Course(name)
        self.courses[name] = course
        return course
        
    def enroll_student(self, student_id: str, student_name: str, course_name: str) -> bool:
        if course_name not in self.courses:
            return False
            
        self.student_names[student_id] = student_name
        course = self.courses[course_name]
        course.enroll_student(student_id)
        return True
        
    def record_grade(self, course_name: str, assignment_name: str, 
                    student_id: str, score: float) -> bool:
        if course_name not in self.courses:
            return False
            
        course = self.courses[course_name]
        for assignment in course.assignments:
            if assignment.name == assignment_name:
                if student_id not in course.enrolled_students:
                    return False
                assignment.add_grade(student_id, score)
                self._check_academic_alert(course_name, student_id)
                return True
        return False
        
    def get_student_average(self, course_name: str, student_id: str) -> Optional[float]:
        if course_name not in self.courses:
            return None
            
        course = self.courses[course_name]
        if student_id not in course.enrolled_students:
            return None
            
        total_score = 0
        total_weight = 0
        
        for assignment in course.assignments:
            if student_id in assignment.grades:
                total_score += assignment.grades[student_id] * assignment.weight
                total_weight += assignment.weight
                
        if total_weight == 0:
            return 0
            
        return total_score / total_weight
        
    def get_course_average(self, course_name: str) -> Optional[float]:
        if course_name not in self.courses:
            return None
            
        course = self.courses[course_name]
        if not course.enrolled_students:
            return None
            
        total = sum(self.get_student_average(course_name, student_id) 
                   for student_id in course.enrolled_students 
                   if self.get_student_average(course_name, student_id) is not None)
                   
        return total / len(course.enrolled_students)
        
    def get_letter_grade(self, percentage: float) -> GradeLevel:
        if percentage >= 90:
            return GradeLevel.A
        elif percentage >= 80:
            return GradeLevel.B
        elif percentage >= 70:
            return GradeLevel.C
        elif percentage > 60:
            return GradeLevel.D
        return GradeLevel.F
        
    def _check_academic_alert(self, course_name: str, student_id: str) -> None:
        average = self.get_student_average(course_name, student_id)
        if not average:
            return
            
        if average < self.courses[course_name].min_passing_grade:
            if student_id not in self.academic_alerts:
                self.academic_alerts[student_id] = []
            if course_name not in self.academic_alerts[student_id]:
                self.academic_alerts[student_id].append(course_name)
        elif student_id in self.academic_alerts and course_name in self.academic_alerts[student_id]:
            self.academic_alerts[student_id].remove(course_name)
            
    def get_missing_assignments(self, course_name: str, student_id: str) -> List[str]:
        if course_name not in self.courses:
            return []
            
        course = self.courses[course_name]
        if student_id not in course.enrolled_students:
            return []
            
        missing = []
        current_date = datetime.now()
        
        for assignment in course.assignments:
            if current_date > assignment.due_date and student_id not in assignment.grades:
                missing.append(assignment.name)
                
        return missing
