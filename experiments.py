import configparser


def return_settings(file_name: str) -> dict:
    configurations = configparser.ConfigParser()
    configurations.read(file_name)
    dictionary_secrets = {}

    for i in configurations:
        for j in configurations[i]:
            dictionary_secrets[j] = configurations[i][j]

    return dictionary_secrets


print(return_settings('credentials.ini'))