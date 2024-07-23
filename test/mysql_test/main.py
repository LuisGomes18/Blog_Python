class MYSQL_CONNECT:
    def __init__(self):
        self.params = {}

    def __setitem__(self, key, value):
        self.params[key] = value

    def connect(self):
        required_params = ['host', 'user', 'password', 'database']

        try:
            # Check if all required parameters are present
            for param in required_params:
                if param not in self.params:
                    raise Exception(f'Missing {param}')

            # Simulate the connection process (replace this with actual connection logic)
            print(f'Connecting to the database at {self.params['host']}:{
                    self.params['port']} with user {self.params['user']}')
            # If connection is successful
            print('Successfully connected to the database')

        except KeyError as e:
            print(f'KeyError: {str(e)}')
        except ValueError as e:
            print(f'ValueError: {str(e)}')
        except Exception as e:
            print(f'An error occurred: {str(e)}')
