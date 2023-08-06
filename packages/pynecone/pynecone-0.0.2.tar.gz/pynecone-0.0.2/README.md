# pynecone

A library to make writing cli applications easier

Usage example:

    from pynecone import Shell, Subshell, Command

    class Login(Command):
    
        def __init__(self):
            super().__init__("login")
    
        def run(self, args):
            print("logging in")
    
    class Logout(Command):
    
        def __init__(self):
            super().__init__("logout")
    
        def run(self, args):
            print("logging out")
    
    
    class Auth(Subshell):
    
        def __init__(self):
            super().__init__("auth")
    
        def get_commands(self):
            return [Login(), Logout()]
    
    
    class Myapp(Shell):
    
        def get_commands(self):
            return [Auth()]
    
    def main():
        Myapp().run()
    
    
    if __name__ == "__main__":
        main()