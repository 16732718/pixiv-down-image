# -*- coding:UTF-8 -*-
import os, zipfile
import ffmpeg
from moviepy.editor import VideoFileClip
from PIL import Image
import base64


def unzipSingle(src_file, dest_dir, password):
    # 解压单个文件到目标文件夹。
    if password:
        password = password.encode()
    zf = zipfile.ZipFile(src_file)
    try:
        zf.extractall(path=dest_dir, pwd=password)
    except RuntimeError as e:
        print(e)
    zf.close()
    # 解压完毕删除源文件
    os.remove(src_file)


# 图片合成视频
def saveVideo(path, pid):
    (ffmpeg
     .input(path + pid + '/*.jpg', pattern_type='glob', framerate=23)
     .filter('scale', size='hd1080', force_original_aspect_ratio='increase')
     .output(path + pid + '.mp4')
     .run()
     )


# 生成webm
def saveWebm(path, pid):
    filelist = os.listdir(path + pid)
    for i, v in enumerate(filelist):
        filelist[i] = path + pid + '/' + v
    clip = VideoFileClip(path + pid + '.mp4')  # mp4转webm
    clip.write_videofile(path + pid + '.webm', bitrate='1000k', verbose=False, audio=False)


# 图片转base64
def toBase64(path, pid):
    img_arr = []
    filelist = os.listdir(path + pid)
    filelist.sort()
    for i, v in enumerate(filelist):
        img_path = path + pid + '/' + v
        with open(img_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            img_arr.append('data:image/jpeg;base64,' + base64_data.decode())
    return img_arr


def saveHtml(path, pid):
    # 命名生成的html
    GEN_HTML = path + pid + ".html"
    img = Image.open(path + pid + '/000000.jpg')
    img_arr = toBase64(path, pid)
    #取一张图片的宽度
    width = img.size[0]
    # 打开文件，准备写入
    f = open(GEN_HTML, 'w')

    # 写入HTML界面中
    message = """
   <!DOCTYPE html>
<html lang="en">
<body>
<canvas id="cvs1" style="text-align: center; display: block;
                margin: 50px auto;">

</canvas>
</body>
<script>
    window.onload = function () {
        playAnimate();
    }

    var cvs = document.getElementById('cvs1');
    cvs.width = "600";//注意：没有单位
    cvs.height = "%s";//注意：没有单位

    var ctx = cvs.getContext('2d');
    var frame = new Image();
    var speed = 1000 / 23.976;


    var timer = null;


    function renderToCanvas() {
        frame.onload = function () {
            var frm = ctx.createPattern(frame, "no-repeat");
            ctx.fillStyle = frm;
            ctx.fillRect(0, 0, 600, 960);

        }
    }

    function playAnimate() {
        let img_arr=%s
        var i = 0;
        timer = setInterval(function () {
            frame.src = img_arr[i]//导入
            renderToCanvas();//渲染到画布
            if (i >= img_arr.length) {
                i = 0
            }
            i += 1

        }, speed);
    }

</script>
</html>
    """ % (width, img_arr)

    # 写入文件
    f.write(message)
    # 关闭文件
    f.close()

# 调用shell生成高质量gif 体积过大
def CreateShelltoGif(path, pid):
    arg1 = path + pid + '.mp4'
    arg2 = path + pid + '.gif'
    os.system('./createGif.sh ' + arg1 + ' ' + arg2)
