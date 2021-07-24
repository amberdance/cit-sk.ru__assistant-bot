import re

print(bool(re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b',"zxc@zs.ru")) is True)