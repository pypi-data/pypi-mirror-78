import sys
import importlib
def main():
    command_dict = {
        'md5':         'yxspkg.md5',
        'fafa-excel':  'yxspkg.fafa_excel',
        'songzigif':   'yxspkg.songzgif.gif',
        'songziviewer':'yxspkg.songziviewer',
        'm3u8':        'yxspkg.m3u8',
        'server':      'yxspkg.file_server.server',
        'video2html':  'yxspkg.video2html',
        'getdata':     'yxspkg.getdata.getdata_qt',
        'convert_url': 'yxspkg.convert_url',
        'image':       'yxspkg.image.image_operator',
        'video':       'yxspkg.video.video_operator'
    }
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        sys.argv.pop(1)
    else:
        cmd = '--help'
    if cmd not in command_dict:
        cmd = '--help'
    if cmd == '--help':
        print('useage:module list')
        for i in command_dict:
            print(i)
    else:
        importlib.import_module(command_dict[cmd]).main()
if __name__=='__main__':
    main()