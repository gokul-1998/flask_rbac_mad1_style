class parent:
    def __init__(self):# constructor
        self.parent = 'I\'m the parent'
        print('Parent')

    def parent_method(self):
        print('This is the parent method')

class parent2:
    def __init__(self):# constructor
        self.parent = 'I\'m the parent'
        print('Parent')

    def parent_method(self):
        print('This is the parent2 method')

class child(parent,parent2):
    def __init__(self): # constructor
        super().__init__()
    
        print('Child')

    def child_method(self):
        print('This is the child method')

# c = child()
# c.child_method()
# c.parent_method()

gokul=parent()
junior_gokul=child()
print(gokul.parent)