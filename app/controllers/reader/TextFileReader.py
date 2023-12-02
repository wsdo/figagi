import glob
from pathlib import Path
from wasabi import msg

def text_load_file(file_path: Path) -> dict:
    """
    读取文本文件。

    @param file_path : Path - 文件路径
    @return dict - 返回包含文件名（键）和其内容（值）的字典
    """
    file_contents = {}
    supported_file_types = [".txt", ".md", ".mdx", ".json"]

    if file_path.suffix.lower() not in supported_file_types:
        msg.warn(f"不支持的文件类型: {file_path.suffix}")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            msg.info(f"正在读取 {str(file_path)}")
            file_contents[str(file_path)] = f.read()
        msg.good(f"已加载 {len(file_contents)} 个文件")
    except IOError as e:
        msg.fail(f"读取文件 {str(file_path)} 时出错: {e}")

    return file_contents

def text_load_directory(dir_path: Path) -> dict:
    """
    从目录及其子目录中读取文本文件。

    @param dir_path : Path - 目录路径
    @return dict - 返回包含文件名（键）和其内容（值）的字典
    """
    file_contents = {}
    supported_file_types = ["txt", "md", "mdx", "json"]

    for file_type in supported_file_types:
        files = glob.glob(f"{str(dir_path)}/**/*.{file_type}", recursive=True)

        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    msg.info(f"正在读取 {file}")
                    file_contents[file] = f.read()
            except IOError as e:
                msg.fail(f"读取文件 {file} 时出错: {e}")

    msg.good(f"已加载 {len(file_contents)} 个文件")
    return file_contents
