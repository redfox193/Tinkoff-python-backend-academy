from collections import defaultdict
from dataclasses import dataclass
from typing import List


class NotFound(Exception):
    pass


@dataclass
class Entity:
    entity_type: str #KISS It's better to derive new specified dataclasses from this base dataclass. 
                     #In that case user won't wrie invalid entity_type and don't have to guess which he should write
    name: str


class IndexGenerator:
    def __init__(self):
        self.current = 0

    def generate_index(self) -> int:  #KISS We can use += operator to make code shorter and more readable
        self.current = self.current + 1
        return self.current


class CourseManagementSystem:
    def __init__(self):
        self.igen = IndexGenerator()
        self.teachers_table = {}  #YAGNI We do not need to create different tables for students and teachers as they share
        self.students_table = {}  #the same general id generator. And students_table is not useful as teacher_table. And we have entity_type to differ members
        self.student_teacher_assignment_table = defaultdict(list)

    def next_index(self):
        return self.igen.generate_index()

    def create_entity(self, entity: Entity) -> int:
        next_index = self.next_index()
        if entity.entity_type == 'teacher': #KISS the problem I've mentioned above. It's hard for user to guess which entity_type he should write 
            self.teachers_table[next_index] = entity
        else:
            self.students_table[next_index] = entity
        return next_index

    def find_entity(self, entity_id) -> Entity:
        if entity_id in self.teachers_table:
            return self.teachers_table[entity_id]

        return self.students_table[entity_id]

    def assign_student(self, s_entity_id: int, t_entity_id: int):
        teacher = self.find_entity(t_entity_id)  #YAGNI We do not have to assign return value to variables as we do not use them
        student = self.find_entity(s_entity_id)

        self.student_teacher_assignment_table[t_entity_id].append(s_entity_id) #KISS It's better to assign by name as it's required in the assignment
                                                                               #we do not get profit from using ids as when we are looking for teacher, we use name

    def count_assigned_students(self, entity_id: int) -> int:  #YAGNI in our task we do not need to count assigned students
        teacher = self.find_entity(entity_id)

        return len(self.student_teacher_assignment_table[entity_id])

    def list_assigned_students(self, name: str) -> List[str]:
        for k, v in self.teachers_table.items():
            if v.name == name:
                return self.student_teacher_assignment_table[k]
        raise NotFound('teacher not found')