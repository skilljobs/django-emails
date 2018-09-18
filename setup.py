from setuptools import setup, find_packages
import emails

setup(
    name='emails',
    version=emails.__version__,
    description='Mailing and processing for high volume senders and recipients.',
    long_description=open('README.rst').read(),
    license='BSD License',
    platforms=['OS Independent'],
    keywords='email,dkim,imap,subscriptions,bounces',
    author='fmalina',
    author_email='fmalina@gmail.com',
    url='https://github.com/fmalina/emails',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split(),
)
