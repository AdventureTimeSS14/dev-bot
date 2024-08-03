import configparser

config = configparser.ConfigParser()
config.read('config.ini')
DISCORD_KEY = config['KEY']['DISCORD_KEY']
