import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pathlib import Path

import yaml  # type: ignore
from fastapi import APIRouter

from config.settings import app_settings
from server import contracts

router = APIRouter()


class Iterator(ABC):
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def __iter__(self) -> 'Iterator':
        return self

    @abstractmethod
    def __next__(self) -> tuple[str, list[str]]:
        ...


class IteratorXML(Iterator):
    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        self.person_iter = iter(self.root.findall(".//person"))

    def __next__(self) -> tuple[str, list[str]]:
        person_element = next(self.person_iter, None)

        if person_element is None:
            raise StopIteration

        parent_name = person_element.attrib.get("name")
        children = [
            child.attrib.get("name")
            for child in person_element.findall(".//child")
        ]

        return parent_name, children


class IteratorYML(Iterator):
    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = yaml.safe_load(file)
        self.person_iter = iter(self.data.get("persons", []))

    def __next__(self) -> tuple[str, list[str]]:
        person_data = next(self.person_iter, None)

        if person_data is None:
            raise StopIteration

        parent_name = person_data.get("name", "")
        children_data = person_data.get("children", [])
        children = [child.get("name", "") for child in children_data]

        return parent_name, children


class IteratorJSON(Iterator):
    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        self.person_iter = iter(self.data.get("persons", []))

    def __next__(self) -> tuple[str, list[str]]:
        person_data = next(self.person_iter, None)

        if person_data is None:
            raise StopIteration

        parent_name = person_data.get("name", "")
        children_data = person_data.get("children", [])
        children = [child.get("name", "") for child in children_data]

        return parent_name, children


class IteratorFactory:
    @staticmethod
    def create_iterator(file_path: Path) -> Iterator | None:
        file_extension = file_path.suffix.lower()
        match file_extension:
            case ".xml":
                return IteratorXML(file_path)
            case ".yml":
                return IteratorYML(file_path)
            case ".json":
                return IteratorJSON(file_path)
            case _:
                return None


@router.get("/parents/{child_name}", response_model=contracts.FoundParents)
async def find_parent(child_name: str) -> contracts.FoundParents:
    parents = []
    for file_path in Path(app_settings.app_files_dir).rglob("*"):
        if file_path.is_file():
            file_iterator = IteratorFactory.create_iterator(file_path)
            if file_iterator is None:
                continue

            for parent, children in file_iterator:
                if child_name in children:
                    parents.append(parent)

    return contracts.FoundParents(found_parents=parents)
