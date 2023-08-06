try:
    from setuptools import setup, find_namespace_packages
except ModuleNotFoundError as e:
    print(e.msg)
    exit()

with open("README.md", "r") as re:
    long_dis = re.read()

setup(
    name="webtree-sg",
    version=1.0,
    author="shivam goswami",
    author_email="shivamgoswami2711@gmail.com",
    description="A simple websiteStructure meker written in python.",
    long_description=long_dis,
    install_requires=['prompt_toolkit==1.0.14','PyInquirer','colorama', 'examples'],
    include_package_data=True,
    python_requires='>=3.5',
    packages=["webtree-sg"],
    classifiers=[
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Office/Business'
          ],

)