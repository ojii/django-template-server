from setuptools import setup
from templateserver import __version__ as version

with open('README.rst') as fobj:
    long_description = fobj.read() 


setup(name="django-template-server",
      version=version,
      description="Makes it easy to test Django templates",
      long_description=long_description,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='django templates',
      author='Jonas Obrist',
      author_email='jonas.obrist@divio.ch',
      url='http://github.com/ojii/django-template-server',
      license='BSD',
      packages=['templateserver'],
      entry_points=dict(console_scripts=['maketemplateserver=templateserver.maketemplateserver:main']),
      install_require=['virtualenv>=1.6'],
      zip_safe=False)
