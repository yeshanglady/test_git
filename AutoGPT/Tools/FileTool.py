import os
def list_files_in_directory(path: str) -> str:
    """
    列出指定目录下的所有文件
    :param path: 目录路径
    :return: 文件列表
    """
    if not os.path.exists(path):
        return "目录不存在"
    files = os.listdir(path)
    return "\n".join(files)