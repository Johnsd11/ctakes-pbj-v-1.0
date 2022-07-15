import configparser
config = configparser.RawConfigParser()
config.read("src/main/resources/pipeline/ctakes_const.py")

print(config.get("NE", "NE_TYPE_ID_UNKNOWN"))

