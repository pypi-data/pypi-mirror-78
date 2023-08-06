from ffmpeg_sdk import log, run_shell


def prune(file_name, output, start_time=0):
    """
    :param file_name: 剪切的文件
    :param output: 输出文件
    :param start_time: 剪切开始的时间
    :return :
    """

    shell = (
        'ffmpeg '
        '-y '
        '-ss {} '
        '-i {} '
        '-c:a copy '
        '-c:v copy '
        '{}'
    ).format(start_time, file_name, output)
    log.info(shell)
    run_shell(shell)

    return output
