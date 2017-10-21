import os


def get_userdir_filename(fn_basename):
    final_fn = os.path.abspath(os.path.expanduser("~/.{}".format(fn_basename)))
    return final_fn


def get_filename_relative_to_sentinal(path, sentinal, conf_filename):
    while path != "/":
        if sentinal in os.listdir(path):
            conf_path = os.path.abspath(os.path.join(path, conf_filename))
            if os.path.isfile(conf_path):
                return conf_path
            else:
                return None
        path = os.path.split(path)[0]
    return None


def get_best_filename(array_of_filenames):
    for fn in array_of_filenames:
        if fn is not None and os.path.isfile(fn):
            return fn
    else:
        return None
