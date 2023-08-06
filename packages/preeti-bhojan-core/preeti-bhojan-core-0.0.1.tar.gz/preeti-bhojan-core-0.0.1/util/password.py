import bcrypt

"""
Utilities for hashing and checking password. These functions are 
defined so that the main logic do not need to care about the hashing 
algorithm or policy and can focus on their logic
"""


def hash_password(password):
    """
    It returns the hash of the password given as input. Length of password
    should not be more than 70 characters.
    :param password: the password to hash
    :return: hash of given password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def is_correct(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
