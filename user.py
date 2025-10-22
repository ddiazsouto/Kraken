import secrets


users = {
    'SupremeOverlord':'master_home.html'
}


class User():

    def __init__(self):

        self.nm=''
        self.home_template=''
        self.user_access_key = None

        
    def check(self, login, passwd):

        clave='123'

        if login in users and passwd == clave:

            department = users[login]
            print(department)
            self.home_template = users[login]

            return True


    def name(self):

        return self.nm


    def generate_access_key(self):

        self.user_access_key = secrets.token_hex(16)
        return self.user_access_key        


    def department(self):

        return self.home_template



class ListForm():

    def __init__(self):

        self.many=[]
        self.pairing=dict()

    def employee(self, stringin):

        # for i in DanSQL().get(stringin):
        #     fname=i[0]+' '+i[1]
        #     self.pairing[i[2]]=fname
                
        # while (len(self.pairing)>0):
        #     self.many.append(self.pairing.popitem())

        return self.many


    def client(self, stringin):

        # for i in DanSQL().get(stringin):
        #     nature=i[1]
        #     self.pairing[nature]=i[0]
        
        # while (len(self.pairing)>0):
        #     self.many.append(self.pairing.popitem())

        return self.many
