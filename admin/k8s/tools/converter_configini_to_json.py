import configparser

config = configparser.ConfigParser()
config.read('config/main.ini')

config_dict = {section: dict(config.items(section)) for section in config.sections()}
config_dict['General']['stage'] = "production"
config_dict = str(config_dict).replace("'", "\"")
print(config_dict)
