from collections import defaultdict
from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod


class NotFound(Exception):
    pass


class InvalidMember(Exception):
    pass

# Now we use specified dataclasses for creating different members without nessesarity of writing entity_type by ourself
@dataclass
class Entity(ABC):
    name: str
    @property
    @abstractmethod
    def ROLE(self):
        pass


@dataclass
class Teacher(Entity):
    ROLE: str = "teacher"


@dataclass
class Student(Entity):
    ROLE: str = "student"


class IndexGenerator:
    def __init__(self):
        self.current = 0

    def generate_index(self) -> int:
        self.current += 1  #solved
        return self.current


class CourseManagementSystem:
    def __init__(self):
        self.igen = IndexGenerator()
        self.course_members_table: dict[int, Entity] = {}  #Now we use one table for all members and one index generator for this table
        self.student_teacher_assignment_table: dict[str, list[str]]= defaultdict(list)

    def next_index(self):
        return self.igen.generate_index()

    def create_entity(self, entity: Entity) -> int:
        next_index = self.next_index()
        self.course_members_table[next_index] = entity
        return next_index

    def find_entity(self, entity_id: int):
        if entity_id in self.course_members_table:
            return self.course_members_table[entity_id]
        else:
            raise NotFound('no such member in course')

    def check_member_role(self, entity: Entity, role: Entity.ROLE, message: str):
        if(entity.ROLE != role):
            raise InvalidMember(message)

    def modify_entity(self, entity_id: int, entity: Entity) -> Entity: #We have to add function to modify existing members according to the task
        member = self.find_entity(entity_id)
        self.check_member_role(member, entity.ROLE, "trying to modify member with another role")
        member.name = entity.name
        return member

    def assign_student(self, s_entity_id: int, t_entity_id: int):
        teacher = self.find_entity(t_entity_id)
        self.check_member_role(teacher, Teacher.ROLE, "member is not a teacher")
        student = self.find_entity(s_entity_id)
        self.check_member_role(student, Student.ROLE,"member is not a student")
        self.student_teacher_assignment_table[teacher.name].append(student.name)

    def list_assigned_students(self, name: str) -> List[str]:
        for member in self.course_members_table.values():
            if member.ROLE == Teacher.ROLE and member.name == name:
                return self.student_teacher_assignment_table[name]
        raise NotFound("teacher not found")