import paramiko
from base.main_functions import correct_py_file


def uploader(context, file_name, file_dir):
    """upload file to the server"""
    host = context.custom_config['server']['host']
    port = context.custom_config['server']['port']
    password = context.custom_config['server']['password']
    username = context.custom_config['server']['username']
    with paramiko.Transport((host, int(port))) as transport:
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        remotepath = f'{context.custom_config["server_dir"]}{file_name}'
        localpath = f'{file_dir}/{file_name}'
        sftp.put(localpath, remotepath)
        sftp.close()

def runner(context, file_name):
    """run .py through the django project"""
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=context.custom_config['server']['host'],
            port=context.custom_config['server']['port'],
            username=context.custom_config['server']['username'],
            password=context.custom_config['server']['password']
        )
        command = f'cd {context.custom_config["dir_django_proj"]} && ' \
                  f'python3 manage.py shell < {context.custom_config["server_dir"]}{file_name}'
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()  # Blocking call
        if exit_status == 0:
            print("The creation is finished")
            return True
        else:
            print("Error", exit_status)
            return False

def change_db_through_django(context, file_name, file_dir):
    """upload .py to the server and run it"""
    file_name = file_name + '.py'
    # upload file
    uploader(context, file_name, file_dir)
    # run file
    return runner(context, file_name)


# def download_from_server(file_name):
#     """download"""
#     host = config["server"]["host"]
#     port = config["server"]["port"]
#     username = config["server"]["user"]
#     password = config["server"]["secret"]
#
#     with paramiko.Transport((host, int(port))) as transport:
#         transport.connect(username=username, password=password)
#         sftp = paramiko.SFTPClient.from_transport(transport)
#
#         remotepath = f'{config["server_dir"]["path"]}{file_name}'
#         localpath = f'./base/files_for_ssh/{file_name}'
#         sftp.get(remotepath, localpath)
#
#         sftp.close()
#



def upload_files_server(context):
    old_new_parts={
        '{PATH}': context.custom_config['server_dir']
    }
    correct_py_file("loader", old_new_parts)
    files_list = {
        'accounts.csv': './base/data_set',
        'fees.csv': './base/data_set',
        'main_users.csv': './base/data_set',
        'services.csv': './base/data_set',
        'user_bills.csv': './base/data_set',
        'userdata.csv': './base/data_set',
        'users.csv': './base/data_set',
        'manager_id.txt': './base/data_set',
        'loader.py': './base/files_for_ssh',
        'cleaner.py': './base/files_for_ssh',
        'prop.xlsx': './base/data_set'
    }

    for file_name, file_dir in files_list.items():
        uploader(context, file_name=file_name, file_dir=file_dir)




































