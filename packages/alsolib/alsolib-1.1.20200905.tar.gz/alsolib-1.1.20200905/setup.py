from distutils.core import setup #如果没有需要先安装
setup(name='alsolib',  #打包后的包文件名
      version='1.1.20200905',  #版本
     description='爱搜库1.1.20200905，请使用python原版下载',
      author='asunc',
      author_email='3182305655@qq.com',
      url='http://www.asunc.cn',
      py_modules=['alsolib\\alsoapi','alsolib\\alsolib','alsolib\\alsoxes','alsolib\\alsoqq'],  #与前面的新建文件名一致
)