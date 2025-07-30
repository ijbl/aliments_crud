import jpype

class Aliment:
    '''
    Class representing an Aliment
    '''

    def __init__(self, *args, **kwargs):
        '''
        Aliment's initializer. Its parameters are dynamic because it could be used from serializer and from tests.
        '''
        self.id = 0
        self.name = ''
        self.description = ''
        self.status = False
        if len(args) == 3 and \
           (isinstance(args[0], str) or isinstance(args[0], jpype.java.lang.String)) and \
           (isinstance(args[1], str) or isinstance(args[1], jpype.java.lang.String)) and \
           (isinstance(args[2], bool) or isinstance(args[2], jpype.java.lang.Boolean)):
            self.id = 0
            self.name = args[0]
            self.description = args[1]
            self.status = args[2]
        elif len(args) == 4 and \
            (isinstance(args[0], int) or isinstance(args[0], jpype.java.lang.Integer)) and \
            (isinstance(args[1], str) or isinstance(args[1], jpype.java.lang.String)) and \
            (isinstance(args[2], str) or isinstance(args[2], jpype.java.lang.String)) and \
            (isinstance(args[3], bool) or isinstance(args[3], jpype.java.lang.Boolean)):
            self.id = args[0]
            self.name = args[1]
            self.description = args[2]
            self.status = args[3]
        else:
            if 'id' in kwargs:
                self.id = kwargs['id']
            if 'name' not in kwargs:
                raise ValueError('name field is mandatory')
            self.name = kwargs['name']
            if 'description' in kwargs:
                self.description = kwargs['description']
            if 'status' not in kwargs:
                raise ValueError('status field is mandatory')
            self.status = kwargs['status']



