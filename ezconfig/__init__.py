import os

def get_userdir_filename(fn_basename):
    return os.path.expanduser("~/.{}".format(fn_basename))


def get_filename_relative_to_sentinal(path, sentinal, conf_filename):
    while path != "/":
        print path
        if sentinal in os.listdir(path):
            conf_path = os.path.abspath(os.path.join(path, conf_filename))
            if os.path.isfile(conf_path):
                return conf_path
            else:
                return conf_path, False
        path = os.path.split(path)[0]
    return None
