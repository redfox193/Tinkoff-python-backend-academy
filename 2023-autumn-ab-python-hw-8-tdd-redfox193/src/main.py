from typing import Any


class Node:
    def __init__(self, value: Any = None) -> None:
        self.value = value
        self.next: Node | None = None


class LinkedList:
    def __init__(self, value: Any = None) -> None:
        if value is not None:
            self.head = Node(value)
        else:
            self.head = None

    def to_list(self) -> list:
        new_list = []
        cur_node = self.head
        while cur_node is not None:
            new_list.append(cur_node.value)
            cur_node = cur_node.next
        return new_list

    def append(self, value: Any) -> None:
        last_node = Node(value)
        if self.head is None:
            self.head = last_node
            return
        cur_node = self.head
        while cur_node.next is not None:
            cur_node = cur_node.next
        cur_node.next = last_node

    def prepend(self, value: Any) -> None:
        first_node = Node(value)
        if self.head is None:
            self.head = first_node
            return
        first_node.next = self.head
        self.head = first_node

    def __len__(self) -> int:  # additional extra function for convenience
        size = 0
        cur_node = self.head
        while cur_node is not None:
            size += 1
            cur_node = cur_node.next
        return size

    def find_by_value(self, value: Any) -> int:
        ind = -1
        i = 0
        cur_node = self.head
        while cur_node is not None:
            if cur_node.value == value:
                ind = i
                break
            cur_node = cur_node.next
            i += 1
        return ind

    def __validate_index(
        self, index: int, func: str
    ) -> int:  # additional function to prevent code duplication
        if type(index) is not int:
            raise TypeError("LinkedList.{0}: index must be of type int".format(func))
        size = len(self)
        if index >= size or index < -size:
            raise IndexError("LinkedList.{0}: index out of range".format(func))
        if index < 0:
            index += len(self)
        return index

    def __find_by_index(
        self, index: int
    ) -> Node:  # also private function to prevent code duplication
        index = self.__validate_index(index, "find_by_index(index)")
        cur_node = self.head
        while index != 0:
            cur_node = cur_node.next
            index -= 1
        return cur_node

    def find_by_index(self, index: int) -> Any:
        return self.__find_by_index(index).value

    def delete_by_index(self, index: int) -> None:
        index = self.__validate_index(index, "delete_by_index(index)")
        if index == 0:
            self.head = self.head.next
            return
        prev_node = self.__find_by_index(index - 1)
        prev_node.next = prev_node.next.next

    def delete_by_value(self, value: Any) -> None:
        if self.head is None:
            raise ValueError("LinkedList.delete_by_value(value): value is not in LinkedList")
        if self.head.value == value:
            self.head = self.head.next
            return

        cur_node = self.head
        while cur_node.next is not None and cur_node.next.value != value:
            cur_node = cur_node.next

        if cur_node.next is None:
            raise ValueError("LinkedList.delete_by_value(value): value is not in LinkedList")
        cur_node.next = cur_node.next.next

    def insert(self, value, index: int) -> None:
        if type(index) is not int:
            raise TypeError("LinkedList.insert(value, index): index must be of type int")
        size = len(self)

        if index < 0:
            index += size
            index = max(index, 0)
        else:
            index = min(index, size)

        if index == 0:
            self.prepend(value)
            return

        insert_node = Node(value)
        prev_node = self.__find_by_index(index - 1)
        insert_node.next = prev_node.next
        prev_node.next = insert_node

    def reverse(self) -> None:
        if self.head is None or self.head.next is None:
            return

        prev_node = self.head
        cur_node = prev_node.next
        prev_node.next = None
        next_node = cur_node
        while cur_node.next is not None:
            next_node = cur_node.next
            cur_node.next = prev_node
            prev_node = cur_node
            cur_node = next_node
        next_node.next = prev_node
        self.head = next_node

    def remove_dublicates(self) -> None:
        if self.head is None or self.head.next is None:
            return
        cur_node = self.head
        while True:
            node = cur_node
            while node.next is not None:
                if node.next.value == cur_node.value:
                    node.next = node.next.next
                    continue
                node = node.next
            if cur_node.next is None:
                break
            cur_node = cur_node.next

    def count(self, value: Any) -> int:
        cur_node = self.head
        kol = 0
        while cur_node is not None:
            if cur_node.value == value:
                kol += 1
            cur_node = cur_node.next
        return kol

    def get_from_end(self, k: int) -> Any:
        if type(k) is not int:
            raise TypeError("LinkedList.get_from_end(k): k must be of type int")
        if k < 0:
            raise ValueError("LinkedList.get_from_end(k): k must be greater than 0")
        index = len(self) - k - 1
        if index < 0:
            raise IndexError("LinkedList.get_from_end(k): k is out of range")
        return self.__find_by_index(index).value
