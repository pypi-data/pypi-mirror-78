from os import path
import configparser

__all__ = [
    'config'
]


config = configparser.ConfigParser()

if path.isfile('wafec-fi-hypothesis.ini'):
    config.read('wafec-fi-hypothesis.ini')