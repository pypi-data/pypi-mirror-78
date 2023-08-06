import os


def prepare():
    print("prepare...")


def commit():
    try:
        print("create .gitignore, add ignore files")
        os.system("git init")
        os.system("git add *")
        os.system("git commit -m 'first commit'")
        os.system("git branch -M master")
        os.system("git remote add origin git@github.com:jxs1211/pyeventbus.git")
        os.system("git push -u origin master")
        # 如果push失败，使用如下命令强制提交
        os.system("git push -f")
    except Exception as e:
        raise e


def setup():
    """ 
    python3 setup.py sdist bdist_wheel
     """
    try:
        os.system('python3 setup.py sdist')
    except Exception as e:
        raise e


def upload():
    """ 
    twine check dist/*
    twine upload dist/*
    """
    try:
        os.system('twine check dist/*')
        os.system('twine upload dist/*')
    except Exception as e:
        raise e


def clearup():
    print("clearup...")


def test():
    # # 安装最新的版本测试
    # pip install -U example_pkg -i https://pypi.org/simple
    pass


def do_package():
    prepare()
    setup()
    upload()
    clearup()
    # test()


if __name__ == "__main__":
    do_package()
