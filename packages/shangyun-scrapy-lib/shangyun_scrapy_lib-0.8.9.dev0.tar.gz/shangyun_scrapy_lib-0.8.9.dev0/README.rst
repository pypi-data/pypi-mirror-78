上传过程记录


python3 setup.py sdist bdist_wheel

发布Python 包
1.在Home新建一个隐藏文件名为.pypirc，写入PyPi账户以及密码信息，这样每次上传不需要再繁琐的输入用户名和密码了。

[distutils]
index-servers = pypi

[pypi]
username:your_username
password:your_password

2.本地测试

``
python setup.py install
``

3.注册包

上传前需要注册一下包的名称，因为这个名称必须独一无二，如被占用则注册不通过。
python setup.py register
4.检测是否符合Pypi要求


twine check dist/**_.tar.gz

5.上传

twine upload dist/**_.tar.gz
完成上传你就可以在Pypi上看到你上传的包了。并且可以使用pip install安装你的包了。