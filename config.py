import yaml


class Config:
    def __init__(self):
        self.config_data = None
        with open("config/config.yaml", "r") as stream:
            try:
                self.config_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        self.data_server_url = self.config_data['data_server_url']

        self.login_data = None
        with open("login.yaml", "r") as stream:
            try:
                self.login_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        self.username = self.login_data['username']
        self.password = self.login_data['password']


global_config = Config()
