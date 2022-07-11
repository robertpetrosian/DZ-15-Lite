import functions

def test_get_random_index():
    lst = functions.get_random_index()
    assert isinstance(lst, list)  # it is list
    assert len(lst) == 4  # length = 4
    assert len(lst) == len(set(lst))  #unique

def test_print_cell():
    assert functions.print_cell(0) == ' . '
    assert functions.print_cell(1) == ' 1 '
    assert functions.print_cell(10) == '10 '
    assert functions.print_cell(-10) == ' * '
