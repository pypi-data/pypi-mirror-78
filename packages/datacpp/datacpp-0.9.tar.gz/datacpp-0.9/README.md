this is README.md
python setup.py sdist  bdist_wheel
pip install packages

在https://pypi.org/ 和https://test.pypi.org/ 上注册账号，账号名和密码可以相同
在用户目录下创建.pypirc
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: 用户名
password: 密码

twine upload dist/*
