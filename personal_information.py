class PersonalInformation:

    def __init__(self):
        self.name = "Antonio J. Silva Paucar"
        self.email = 'antonios@uoregon.edu'
        self.github = "WHAAUIZ"
        self.title = "PetiteURL"

    def dict(self):
        return self.__dict__

a = PersonalInformation()


