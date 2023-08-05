rapidapi_key = None


def get_key():
    global rapidapi_key

    if not rapidapi_key:
        rapidapi_key = input("Please enter your RapidAPI Key: ")
    return rapidapi_key


def reset_key():
    global rapidapi_key

    rapidapi_key = input("Wrong key! Please enter the correct one: ")
    return rapidapi_key
