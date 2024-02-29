#!/usr/bin/python3
"""FAbric script that create and distribute an archive to web servers"""
from fabric.api import env, task
from os.path import exists
from datetime import datetime
from fabric.operations import local, put, run

env.hosts = ['35.168.3.210', '52.91.135.13']
env.user = 'ubuntu'
env.key_filename =  '/home/james/.ssh'

def do_pack():
    """Creates a compressed archive of the web_static foleder"""
    