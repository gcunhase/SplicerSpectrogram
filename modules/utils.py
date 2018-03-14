
import os

__author__ = "Gwena Cunha"


def project_dir_name():
    """ Get project directory name

    :return: name of project directory
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.abspath(current_dir + "/../") + "/"
    return project_dir
