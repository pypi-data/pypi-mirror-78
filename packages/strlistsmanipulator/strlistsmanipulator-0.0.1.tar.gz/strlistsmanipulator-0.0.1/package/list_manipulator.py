def lower_and_remove_spaces(string_list):
    """Modify elements in list to be 'abc_def' from 'Abc def'.   

    Note
    ----
    It doesn't consider element at index 0.
    It also eliminates some other special character, for the re.sub function: plus sign, brackets.

    Examples
    --------
    >>> list_test = ["Test1", "Second test", "3rd Test"]
    >>> lower_and_remove_spaces(list_test)
    >>> print(list_test)
    ['Test1', 'second_test', '3rd_test']
    
    Parameters:     
    ----------
    entities_list : list[str]
        List of all the entities
    """     
    for i in range(1, len(string_list)):
        string_list[i] = re.sub("\s", "_", str(string_list[i]))
        string_list[i] = re.sub("\+", "", str(string_list[i]))
        #string_list[i] = re.sub("[()]", "", str(string_list[i]))
        string_list[i] = string_list[i].lower()

def write_result_in_sheet(worksheet, list_field_to_write, index):
    """Write in worksheet.

    Parameters:     
    ----------
    Worksheet : object
        The worksheet to write in
    List_field_to_write : list[str]  
        The list of fields to write in the worksheet (they'll be written in the same row, increasing columns)
    Index : int
        The index of the row in which evrything will be written
    """  
    for i in range(0, len(list_field_to_write)):        
        worksheet.write(index, i, list_field_to_write[i])

def substitute_and_add_hyphen(list_field_to_write, field_to_match, message):
    """Substitute the field_to_match in the message with the first not empty list_field_to_write in this f-o-r-m-a-t.     
    
    Examples
    --------
    >>> print(substitute_and_add_hyphen(["", "substitution"], "match", "the match in the sentence"))
    the s-u-b-s-t-i-t-u-t-i-o-n in the sentence

    Parameters:  
    ----------   
    list_field_to_write  : list[str] 
        The list of field to substitude in the message.
        The first not empty will be selected and each letter will be alternated with a '-'
    field_to_match : str
        The text of the entity to match in messsage
    message : str
        The complete message

    Returns:
    ----------     
       str: The message with the substitution
    """  
    for i in range(0, len(list_field_to_write)):
        if (len(list_field_to_write[i]) > 0) :
            substi = list_field_to_write[i].replace("", "-")[1: -1]
            return re.sub(str(field_to_match), str(substi), str(message))


def _delete(lists, index):
    """private function that is called by delete_on_condition to delete all items in the index in all the list of lists.     
    
    Parameters:     
    ----------
    lists : lists[lists]  
        the list of the list from which some elements will be
    index : int
        the index of all the elements to delete
    """  
    for i in range(0, len(lists)):
        lists[i].pop(index)

def delete_on_condition(list_condition, list_of_list, condition):
    """All the list of list_of_list will have elements at index n deleted of the nth elements of
    list_condition returns True when evaluated with condition.

    The condition parameter was only tested with the lambda operator. 
    Some example of possible condition to be passed are: (lambda a: a == 'NA') or (lambda a: a == True)

    Note
    ----
    It doesn't consider element at index 0.

    Examples
    --------
    >>> print(condition_list, list_a, list_b, list_c)
    [0, 1, 2, 3, 4] ['a', 'b', 'c', 'd', 'e'] [1, 10, 100, 1000, 10000] [0, 1, 0, 1, 0]
    >>> delete_on_condition(condition_list, [list_a, list_b, list_c], (lambda a: a % 2 == 0))
    >>> print(condition_list, list_a, list_b, list_c)
    [0, 1, 2, 3, 4] ['a', 'b', 'd'] [1, 10, 1000] [0, 1, 1]   
    
    Parameters:     
    ----------
    list_condition : list 
        The list of elements to be tested on the condition.
    list_of_list
        The list of all the list that will have elements deleted if the condition is true.
    condition                    
        The condition on which the list_condition will be tested.
    """  
    length_list = len(list_condition)
    for j in reversed(range(1, length_list)):
        if (condition(list_condition[j])):
            _delete(list_of_list, j)