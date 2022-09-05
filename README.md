# podfile
用python 编辑 Podfile文件，包括添加source，添加库，修改库等

安装podfile库

pip3 install podfile

开始编辑

引入模块
import podfile

podfile_path = "" #这里传入Podfile的路径
podfile_obj = podfile.Podfile(podfile_path)

找出target
tar = podfile