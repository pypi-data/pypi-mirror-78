import os

from ffmpeg_sdk import log, run_shell


def concat(file_list, output, removed=False):
    """
    :param file_list: 合并的文件列表
    :param output: 输出文件
    :param removed: 合并成功之后是否删除原有的视频文件
    :return :
    """
    file_name_list = _get_file_name_list(file_list, output)

    concat_shell = (
        'ffmpeg '
        '-y -v info -f concat -safe 0 '
        '-i {} -c copy '
        '{}'
    ).format(file_name_list, output)
    log.info(concat_shell)

    run_shell(concat_shell)

    os.remove(file_name_list)
    if removed:
        for file in file_list:
            os.remove(file)

    return output


def _get_file_name_list(file_list, output):
    file_name_list = '{}.list.tmp'.format(output)
    with open(file_name_list, 'w+') as f:
        for file_name in file_list:
            if not os.path.isfile(file_name):
                log.warning('文件%s不存在')
                continue
            f.write('file {}\n'.format(file_name))
    return file_name_list
