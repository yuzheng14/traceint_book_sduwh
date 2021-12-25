import os
import time
import traceback


def path_exist(path: str):
    """
    若路径不存在则创建路径
    Args:
        path: 路径

    Returns:

    """
    if not os.path.exists(path):
        os.makedirs(path)


def log_file(msg: str, file: str):
    """将msg输出到file指定的文件中

    Args:
        msg (str): 输出信息
        file (str): 文件名称及路径
    """
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'{time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())}\t{msg}\n')


def save_image(image_byte: bytes, name: str, image_path: str):
    """保存验证码图片
    参数
    -----------------------
    image_byte:bytes
        要保存的图片二进制数据
    name:str
        保存图片文件名称
    image_path:str
        保存地址/路径
    """
    path_exist(image_path)
    try:
        with open(f'{image_path}/{name}', 'wb') as f:
            f.write(image_byte)
    except Exception:
        traceback.print_exc()
