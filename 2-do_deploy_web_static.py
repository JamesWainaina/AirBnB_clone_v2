#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""
from fabric.api import local, env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['35.168.3.210', '52.91.135.13']
env.user = 'ubuntu'



# def do_pack():
#     """Creates a compressed archive of the web_static folder"""
#     try:
#         timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#         file_name = "versions/web_static_{}.tgz".format(timestamp)
#         local("mkdir -p versions")
#         local("tar -cvzf {} web_static".format(file_name))
#         return file_name
#     except Exception as e:
#         return None


def do_deploy(archive_path):
    """Deploys the archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_no_ext = archive_name.split('.')[0]

        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(archive_name, archive_no_ext))
        run('rm /tmp/{}'.format(archive_name))
        
        # Updated move operation to handle subdirectories
        run('cp -r /data/web_static/releases/{}/web_static/. /data/web_static/releases/{}/'.
            format(archive_no_ext, archive_no_ext))

        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.
            format(archive_no_ext))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
    


# if __name__ == "__main__":
#     archive_path = do_pack()
#     if archive_path:
#         result = do_deploy(archive_path)
#         print(result)
#     else:
#         print("Packaging failed.")
