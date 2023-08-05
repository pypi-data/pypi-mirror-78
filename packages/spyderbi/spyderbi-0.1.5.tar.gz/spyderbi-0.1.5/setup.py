from setuptools import setup,find_packages
try:
	from setuptools import setup
except:
	from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
	name="spyderbi",
	version='0.1.5',
	keywords='bilibili',
	description='a library for who want to use bilibili to research,maybe in the near future,if you find any problem.you can send email to 761326926@qq.com',
	packages=find_packages(),
	AUTHOR_EMAIL = "761326926@qq.com"
)
