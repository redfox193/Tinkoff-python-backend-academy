import pytest

from hw.after import CourseManagementSystem, Teacher, Student, NotFound, InvalidMember


def test_create_teacher():
    cms = CourseManagementSystem()
    teacher = Teacher('Ethan Johnson')

    created_id = cms.create_entity(teacher)
    found_teacher = cms.find_entity(created_id)
    assert found_teacher.name == teacher.name
    assert found_teacher.ROLE == teacher.ROLE


def test_create_student():
    cms = CourseManagementSystem()
    student = Student('Emma Thompson')

    created_id = cms.create_entity(student)
    found_student = cms.find_entity(created_id)

    assert found_student.name == student.name
    assert found_student.ROLE == student.ROLE


def test_assign_students():
    cms = CourseManagementSystem()

    teacher = Teacher('Ethan Johnson')
    teacher_id = cms.create_entity(teacher)

    student_1 = Student('Emma Thompson')
    student_1_id = cms.create_entity(student_1)

    student_2 = Student('Ava Martinez')
    student_2_id = cms.create_entity(student_2)

    student_3 = Student('Sophia Garcia')
    student_3_id = cms.create_entity(student_3)

    cms.assign_student(student_1_id, teacher_id)
    cms.assign_student(student_2_id, teacher_id)
    cms.assign_student(student_3_id, teacher_id)

    assert len(cms.list_assigned_students(teacher.name)) == 3


def test_modify_members():
    cms = CourseManagementSystem()

    teacher = Teacher('Ethan Johnson')
    teacher_id = cms.create_entity(teacher)

    student_1 = Student('Emma Thompson')
    student_1_id = cms.create_entity(student_1)

    student_2 = Student('Ava Martinez')
    student_2_id = cms.create_entity(student_2)

    student_3 = Student('Sophia Garcia')
    student_3_id = cms.create_entity(student_3)

    new_student = Student("John Snow")
    modified_student = cms.modify_entity(2, new_student)
    assert modified_student.name == new_student.name
    
    modified_student = cms.find_entity(2)
    assert modified_student.name == new_student.name


def test_exceptions():
    cms = CourseManagementSystem()

    with pytest.raises(NotFound):
        cms.list_assigned_students('Mister Anderson')

    with pytest.raises(InvalidMember):
        cms.check_member_role(Student("John Snow"), Teacher.ROLE, "not a teacher")

