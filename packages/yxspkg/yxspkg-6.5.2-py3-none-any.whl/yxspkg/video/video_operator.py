import os
import subprocess
import click 
from pathlib import Path

@click.command()
@click.argument('args',nargs=-1)
@click.option('--rotate',default=None,help='旋转视频')
@click.option('--replace',default=False,help='是否替换该文件',is_flag=True)
@click.option('--ffmpeg_parameter','-f',default='-c copy',help='ffmpeg 参数')
def main(args,replace,rotate,ffmpeg_parameter):
    input_file = Path(args[0]).absolute()
    if len(args) > 1:
        output_file = Path(args[1]).absolute()
    else:
        output_file = input_file.parent / (input_file.stem+'_output'+input_file.suffix)
    temp_file = output_file.parent / (output_file.stem+'_temp'+output_file.suffix)
    ffmpeg_i = f'ffmpeg -i "{input_file}" '
    if rotate:
        ffmpeg_command = ffmpeg_i + f' -metadata:s:v:0 rotate={rotate} ' + ffmpeg_parameter +f' "{temp_file}"'
    t = subprocess.call(ffmpeg_command,shell=True)
    assert t == 0
    if replace:
        os.rename(temp_file,input_file)
    else:
        os.rename(temp_file,output_file)

if __name__=='__main__':
    main()