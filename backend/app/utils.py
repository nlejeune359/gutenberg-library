db_string = "postgresql+psycopg2cffi://postgres:example@database:5432/gutenberg"

def union(lst1, lst2):
    final_list = lst1 + lst2
    return final_list

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
