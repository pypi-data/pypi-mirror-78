from ffmpeg_sdk import run_shell


def capture(stream_url, output_jpg, timeout=10):
    """
    :param stream_url:
    :param output_jpg:
    :param timeout: 连接超时时间，单位s
    """
    shell_cmd = (
        'ffmpeg '
        '-y -rw_timeout {} '  # 设置超时时间10s
        '-i {} '
        '-f mjpeg -ss 0 -vframes 1 '
        '{}'
    ).format(timeout * 1000 * 1000, stream_url, output_jpg)
    run_shell(shell_cmd, name='ffmpeg_capture')

    return output_jpg
