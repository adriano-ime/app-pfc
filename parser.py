import re

# Returns a list of lists, the first element of the list is the header
# The other elements are the elements of the table according to the header
def parse_microstack_table(table_string):
    splitted_list = re.split("\+-*\+-*\+\n?",table_string)[2:-1]
    info_list = []
    for element in splitted_list:
        for l in element.split('\n'):
            splitted_by_bar_list = l.split('|')
            if len(splitted_by_bar_list) > 1:
                splitted_by_bar_list_without_whitespace = [x for x in splitted_by_bar_list if x != '']
                splitted_by_bar_list_without_space = [x.replace(" ","") for x in splitted_by_bar_list_without_whitespace]
                info_list.append(splitted_by_bar_list_without_space)  
    return info_list

s = """
+--------------------------------------+------+--------+------------------------------------+--------+---------+
| ID                                   | Name | Status | Networks                           | Image  | Flavor  |
+--------------------------------------+------+--------+------------------------------------+--------+---------+
| e66e2d11-549c-45bd-81a8-ef4bb1cdfdf2 | test | ACTIVE | test=192.168.222.34, 10.20.20.20   | cirros | m1.tiny |
| d6e88494-65b1-411e-bb45-24a4f49ceb63 | test | ACTIVE | test=192.168.222.218, 10.20.20.105 | cirros | m1.tiny |
+--------------------------------------+------+--------+------------------------------------+--------+---------+
"""
s2 = """
+---------+---------+--------------+-----------+---------------+
| Project | Servers | RAM MB-Hours | CPU Hours | Disk GB-Hours |
+---------+---------+--------------+-----------+---------------+
| admin   |       5 |    150208.52 |    293.38 |        293.38 |
+---------+---------+--------------+-----------+---------------+
"""
s3 = ""
l = parse_microstack_table(s3)
print(l)
