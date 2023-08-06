import requests
from prompt_toolkit.shortcuts import ProgressBar

from prompt_toolkit.shortcuts import button_dialog, radiolist_dialog
from prompt_toolkit.shortcuts import input_dialog

from pytube import YouTube
from pytube import Stream
import ffmpeg


def download(file_name, link):
    with open(file_name, "wb") as f:
        with ProgressBar() as pb:
            print("Downloading %s" % file_name)
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                for data in pb(response.iter_content(chunk_size=512), total=int(total_length) / 512):
                    f.write(data)


def main():
    result = button_dialog('YouDown', text='Select the use mode:', buttons=[
        ('One Download', 0)
    ])
    var = result.run()
    if var == 0:
        # https://www.youtube.com/watch?v=3L5ZIzD84rM
        url = input_dialog(
            title='YouDown',
            text='Enter url from youtube video:').run()
        youtube = YouTube(url)
        buttons = []
        for stream in youtube.streams:
            stream: Stream = stream
            res = stream.resolution
            if not res:
                # if audio
                res = stream.abr
            text = '{mime} {res}'.format(mime=stream.mime_type, res=res)
            buttons.append((stream, text))
        result = radiolist_dialog(title=youtube.title, text="Select download format", values=buttons).run()

        # split is simple way to get 'mp4' in 'video/mp4' for example.
        extension = result.mime_type.split('/')[1]
        file_name = '{title}.{extension}'.format(title=result.title, extension=extension)
        download(file_name, result.url)

        result = button_dialog('YouDown', text='Convert to ogg? (using ffmpeg)', )
        stream = ffmpeg.input(file_name)
        nfile_name = file_name[0:file_name.rindex('.')] + '.ogg'
        stream = ffmpeg.output(stream, nfile_name)
        ffmpeg.run(stream)


if __name__ == '__main__':
    main()
    # test url (best server for my region)
    # http://ftp.unicamp.br/pub/libreoffice/stable/6.0.3/deb/x86_64/LibreOffice_6.0.3_Linux_x86-64_deb_helppack_zh-TW.tar.gz
    # download('test.data', 'http://ftp.unicamp.br/pub/libreoffice/stable/6.0.3/deb/x86_64/LibreOffice_6.0.3_Linux_x86-64_deb_helppack_zh-TW.tar.gz')
