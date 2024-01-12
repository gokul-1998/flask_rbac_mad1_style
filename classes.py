class animal: # class is a blueprint of an object
    def __init__(self, name):
        self.name = name

    def has_tail(self):
        return True
    
    

    def __str__(self):
        return self.name

class cat(animal): # OOPS -> Object Oriented Programming Structure - inheritance, polymorphism, encapsulation, abstraction
    def __init__(self, name): # constructor
        self.name = name
        

    def speak(self):
        return self.name + ' says Meow!'


    def __str__(self):
        return self.name

class dog(animal): # class is a blueprint of an object
    def __init__(self, name):
        self.name = name

    def speak(self):
        return self.name + ' says Woof!'


    def __str__(self):
        return self.name

class lion(animal): # class is a blueprint of an object
    def __init__(self, name):
        self.name = name

    def speak(self):
        return self.name + ' says Roar!'


    def __str__(self):
        return self.name

tom=cat('tom')
x=tom.has_tail()
print(x)
