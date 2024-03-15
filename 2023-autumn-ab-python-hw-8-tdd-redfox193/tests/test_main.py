import pytest
from src.main import Node, LinkedList


# Node
def test_should_create_node():
    assert Node() is not None


def test_should_create_node_with_value():
    assert Node(value=10) is not None


def test_should_create_node_with_unset_value():
    assert Node().value is None


def test_should_create_node_with_unset_next_node():
    assert Node().next is None


def test_should_create_node_with_set_value():
    assert Node(10).value == 10
    assert Node("string").value == "string"
    obj = object()
    assert Node(obj).value == obj


# LinkedList
def test_should_create_linked_list():
    assert LinkedList() is not None


def test_should_create_linked_list_with_head_node():
    assert LinkedList(value=10).head is not None


def test_should_create_linked_list_with_correct_head_node():
    assert LinkedList(value=10).head.value == 10
    assert LinkedList(value=10).head.next is None


# to_list
def test_ll_should_be_convertable_to_list():
    ll = LinkedList()
    assert type(ll.to_list()) is list


def test_empty_ll_should_be_convertable_to_empty_list():
    ll = LinkedList()
    assert len(ll.to_list()) == 0


def test_ll_with_one_element_should_be_convertable_to_single_element_list():
    ll = LinkedList(1)
    assert ll.to_list() == [1]


# append
def test_ll_should_not_append_elements_without_set_value():
    ll = LinkedList()
    with pytest.raises(TypeError):
        ll.append()


def test_empty_ll_should_have_last_node_as_head_after_append():
    ll = LinkedList()
    ll.append("last and head node")
    assert ll.head.value == "last and head node"
    assert ll.head.next is None


def test_ll_should_have_correct_size_after_elements_appending():
    ll = LinkedList(1)
    ll.append("value")
    ll.append(None)
    ll.append(4)
    assert len(ll.to_list()) == 4


def test_ll_should_append_new_elements_correctly():
    ll = LinkedList("string")
    ll.append(3)
    ll.append(None)
    assert ll.to_list() == ["string", 3, None]


# prepend
def test_ll_should_not_prepend_elements_without_set_value():
    ll = LinkedList()
    with pytest.raises(TypeError):
        ll.prepend()


def test_empty_ll_should_have_last_node_as_head_after_prepend():
    ll = LinkedList()
    ll.prepend("first and head node")
    assert ll.head.value == "first and head node"
    assert ll.head.next is None


def test_ll_should_have_new_head_node_after_prepend():
    ll = LinkedList("old head node")
    ll.prepend("new head node")
    assert ll.head.value == "new head node"
    assert ll.head.next is not None


def test_ll_should_have_correct_size_after_elements_prepending():
    ll = LinkedList(1)
    ll.prepend("value")
    ll.prepend(None)
    ll.prepend(4)
    assert len(ll.to_list()) == 4


def test_ll_should_prepend_new_elements_correctly():
    ll = LinkedList("string")
    ll.prepend(3)
    ll.prepend(None)
    assert ll.to_list() == [None, 3, "string"]


def test_ll_should_prepend_and_append_elements_correctly():
    ll = LinkedList(1)
    ll.prepend(2)
    ll.append(3)
    ll.prepend(4)
    ll.prepend(5)
    ll.append(6)
    ll.append(7)
    assert ll.to_list() == [5, 4, 2, 1, 3, 6, 7]


@pytest.fixture
def ll():
    ll = LinkedList()
    ll.append(2)
    ll.append(1)
    ll.append(3)
    ll.append(1)
    ll.append(4)
    ll.append(5)
    ll.append(3)
    ll.append(6)
    return ll


# __len__
def test_ll_should_get_correct_size_using_len(ll):
    assert len(ll) == 8


def test_ll_should_get_zero_size_for_empty_list_using_len():
    ll = LinkedList()
    assert len(ll) == 0


def test_ll_should_get_one_size_for_single_element_list_using_len():
    ll = LinkedList("one element list")
    assert len(ll) == 1


# find_by_value
def test_ll_should_not_find_element_by_value_without_set_value():
    ll = LinkedList()
    with pytest.raises(TypeError):
        ll.find_by_value()


def test_ll_should_find_index_of_element_by_value(ll):
    assert ll.find_by_value(4) == 4
    assert ll.find_by_value(5) == 5


def test_ll_should_find_index_of_first_occurence_of_element_by_value(ll):
    assert ll.find_by_value(1) == 1
    assert ll.find_by_value(3) == 2


def test_ll_should_proccess_case_when_there_is_no_such_value(ll):
    assert ll.find_by_value("value") == -1


def test_ll_should_not_find_anything_in_empty_list_by_value():
    ll = LinkedList()
    assert ll.find_by_value(1) == -1


def test_ll_should_find_head_element_by_value(ll):
    assert ll.find_by_value(2) == 0


def test_ll_should_find_tail_element_by_value(ll):
    assert ll.find_by_value(6) == 7


# find_by_index
def test_ll_should_not_find_element_by_index_without_set_index():
    ll = LinkedList()
    with pytest.raises(TypeError):
        ll.find_by_index()


def test_ll_should_find_by_index_not_of_type_int(ll):
    with pytest.raises(TypeError):
        ll.find_by_index("index")
        ll.find_by_index(None)


def test_ll_should_raise_exception_when_searching_in_empty_ll_by_index():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.find_by_index(0)
        ll.find_by_index(1)
        ll.find_by_index(-1)


def test_ll_should_find_element_by_positive_index(ll):
    assert ll.find_by_index(0) == 2
    assert ll.find_by_index(7) == 6
    assert ll.find_by_index(3) == 1


def test_ll_should_find_element_by_negative_index(ll):
    assert ll.find_by_index(-1) == 6
    assert ll.find_by_index(-8) == 2
    assert ll.find_by_index(-4) == 4


def test_ll_should_raise_exeption_when_given_positive_index_is_out_of_range(ll):
    with pytest.raises(IndexError):
        ll.find_by_index(8)


def test_ll_should_raise_exeption_when_given_negative_index_is_out_of_range(ll):
    with pytest.raises(IndexError):
        ll.find_by_index(-9)


# delete by index
def test_ll_should_not_delete_element_by_index_without_set_index():
    ll = LinkedList()
    with pytest.raises(TypeError):
        ll.delete_by_index()


def test_ll_should_delete_by_index_from_empty_list():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.delete_by_index(0)


def test_ll_should_delete_by_index_of_incorrect_type(ll):
    with pytest.raises(TypeError):
        ll.delete_by_index("index")


def test_ll_should_raise_exeption_when_given_positive_index_for_deleting_is_out_of_range(ll):
    with pytest.raises(IndexError):
        ll.delete_by_index(8)


def test_ll_should_raise_exeption_when_given_negative_index_for_deleting_is_out_of_range(ll):
    with pytest.raises(IndexError):
        ll.delete_by_index(-9)


def test_ll_should_delete_element_by_positive_index(ll):
    ll.delete_by_index(0)
    ll.delete_by_index(len(ll) - 1)
    ll.delete_by_index(3)
    assert ll.to_list() == [1, 3, 1, 5, 3]


def test_ll_should_delete_element_by_negative_index(ll):
    ll.delete_by_index(-1)
    ll.delete_by_index(-len(ll))
    ll.delete_by_index(3)
    assert ll.to_list() == [1, 3, 1, 5, 3]


def test_ll_should_delete_all_elements_by_index(ll):
    for _ in range(len(ll)):
        ll.delete_by_index(0)
    assert ll.head is None
    assert ll.to_list() == []


# delete by value
def test_ll_should_not_delete_element_by_value_without_set_value():
    ll = LinkedList()
    with pytest.raises(TypeError):
        ll.delete_by_value()


def test_ll_should_delete_by_value_from_empty_list():
    ll = LinkedList()
    with pytest.raises(ValueError):
        ll.delete_by_value(1)


def test_ll_should_delete_by_value_which_is_not_in_list(ll):
    with pytest.raises(ValueError):
        ll.delete_by_value("value")


def test_ll_should_delete_by_value(ll):
    ll.delete_by_value(4)
    assert ll.to_list() == [2, 1, 3, 1, 5, 3, 6]


def test_ll_should_delete_by_value_many_times(ll):
    ll.delete_by_value(4)
    ll.delete_by_value(5)
    assert ll.to_list() == [2, 1, 3, 1, 3, 6]


def test_ll_should_delete_first_occurence_of_element_by_value(ll):
    ll.delete_by_value(1)
    assert ll.to_list() == [2, 3, 1, 4, 5, 3, 6]


def test_ll_should_delete_more_than_it_has(ll):
    with pytest.raises(ValueError):
        ll.delete_by_value(1)
        ll.delete_by_value(1)
        ll.delete_by_value(1)


def test_ll_should_delete_by_head_value(ll):
    ll.delete_by_value(2)
    assert ll.to_list() == [1, 3, 1, 4, 5, 3, 6]


def test_ll_should_delete_by_tail_value(ll):
    ll.delete_by_value(6)
    assert ll.to_list() == [2, 1, 3, 1, 4, 5, 3]


def test_ll_should_delete_all_elements_by_value(ll):
    ll.delete_by_value(2)
    ll.delete_by_value(1)
    ll.delete_by_value(3)
    ll.delete_by_value(1)
    ll.delete_by_value(4)
    ll.delete_by_value(5)
    ll.delete_by_value(3)
    ll.delete_by_value(6)
    assert ll.head is None
    assert ll.to_list() == []


# insert by index
def test_ll_should_raise_exception_when_inserting_value_by_not_int_index(ll):
    with pytest.raises(TypeError):
        ll.insert("value", "1")


def test_ll_should_insert_value_in_empty_list(ll):
    ll = LinkedList()
    ll.insert(value=10, index=0)
    assert ll.to_list() == [10]


def test_ll_should_insert_value_in_the_end_by_non_negative_index(ll):
    ll.insert(value=10, index=len(ll))
    assert ll.to_list() == [2, 1, 3, 1, 4, 5, 3, 6, 10]


def test_ll_should_insert_value_in_the_begining_by_non_negative_index(ll):
    ll.insert(value=10, index=0)
    assert ll.to_list() == [10, 2, 1, 3, 1, 4, 5, 3, 6]


def test_ll_should_insert_value_by_non_negative_index(ll):
    ll.insert(value="v1", index=2)
    ll.insert(value="v2", index=2)
    ll.insert(value="v3", index=4)
    ll.insert(value="v4", index=100)
    assert [1, 3, "v2", "v1", 1, "v3", 4, 5, 3, 6, "v4"]


def test_ll_should_insert_value_in_the_begining_by_negative_index(ll):
    ll.insert(value=10, index=-len(ll))
    assert ll.to_list() == [10, 2, 1, 3, 1, 4, 5, 3, 6]


def test_ll_should_insert_value_by_negative_index(ll):
    ll.insert(value="v1", index=-2)
    ll.insert(value="v2", index=-2)
    ll.insert(value="v3", index=-4)
    ll.insert(value="v4", index=-100)
    assert ["v4", 2, 1, 3, 1, "v4", 4, 5, "v3", "v1", "v2", 3, 6]


# reverse list
def test_ll_should_reverse_empty_list():
    ll = LinkedList()
    ll.reverse()
    assert ll.to_list() == []


def test_ll_should_reverse_single_element_list():
    ll = LinkedList(1)
    ll.reverse()
    assert ll.to_list() == [1]


def test_ll_should_reverse_double_element_list():
    ll = LinkedList(1)
    ll.append(2)
    ll.reverse()
    assert ll.to_list() == [2, 1]


def test_ll_should_reverse_list(ll):
    reversed_list = ll.to_list()
    reversed_list.reverse()
    ll.reverse()
    assert ll.to_list() == reversed_list


# remove_duplicates
def test_ll_should_remove_duplicates_from_empty_list():
    ll = LinkedList()
    ll.remove_dublicates()
    assert ll.to_list() == []


def test_ll_should_remove_duplicates_from_single_element_list():
    ll = LinkedList(1)
    ll.remove_dublicates()
    assert ll.to_list() == [1]


def test_ll_should_remove_duplicates_when_all_elements_are_equal():
    ll = LinkedList()
    for _ in range(10):
        ll.append("value")
    ll.remove_dublicates()
    assert ll.to_list() == ["value"]


def test_ll_should_remove_duplicates_from_single_list_with_unique_elements():
    ll = LinkedList()
    correct_list = [i for i in range(10)]
    for i in range(10):
        ll.append(i)
    ll.remove_dublicates()
    assert ll.to_list() == correct_list


def test_ll_should_remove_duplicates_from_list(ll):
    ll.remove_dublicates()
    assert ll.to_list() == [2, 1, 3, 4, 5, 6]


# get count kol of elements of given value
def test_ll_should_count_kol_of_elements_of_given_value_in_empty_list():
    ll = LinkedList()
    assert ll.count("no such value") == 0


def test_ll_should_count_kol_of_elements_of_given_value_when_there_is_no_such_value(ll):
    assert ll.count("no such value") == 0
    assert ll.count(10) == 0
    assert ll.count(object()) == 0


def test_ll_should_count_kol_of_elements_of_given_value(ll):
    assert ll.count(1) == 2
    assert ll.count(2) == 1
    assert ll.count(3) == 2
    assert ll.count(6) == 1


# get k-th element from end of the list
def test_ll_should_raise_exeption_while_getting_k_th_element_with_incorrect_k_type(ll):
    with pytest.raises(TypeError):
        ll.get_from_end("1")


def test_ll_should_raise_exeption_while_getting_k_th_element_with_negative_k(ll):
    with pytest.raises(ValueError):
        ll.get_from_end(-1)


def test_ll_should_raise_exeption_while_getting_k_th_element_from_the_end_if_list_is_empty():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get_from_end(0)


def test_ll_should_raise_exeption_while_getting_k_th_element_from_the_end_if_k_is_out_of_range(ll):
    with pytest.raises(IndexError):
        ll.get_from_end(len(ll))


def test_ll_should_get_first_element_from_the_end_in_single_element_list(ll):
    ll = LinkedList("value")
    assert ll.get_from_end(0) == "value"


def test_ll_should_get_element_from_the_end_list(ll):
    assert ll.get_from_end(0) == 6
    assert ll.get_from_end(len(ll) - 1) == 2
    assert ll.get_from_end(4) == 1
