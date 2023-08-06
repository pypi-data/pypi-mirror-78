from setuptools import setup, Extension

# python setup.py sdist bdist_wheel
# twine upload dist/*

module = Extension('virxrlcu', sources=['virxrlcu.c'])

setup(name='VirxERLU-CLib',
      version='1.8.0',
      description='C modules for VirxERLU',
      long_description="""
Big thanks to ddthj/GoslingUtils for the basis of VirxERLU. This version, however, improves upon many things, including pathfinding, finding shots, and aerials.
VirxERLU-CLib is the C library for VirxERLU.
""",
      ext_modules=[module],
      license="MIT",
      author='VirxEC',
      author_email='virx@virxcase.dev',
      url="https://github.com/VirxEC/VirxERLU",
      python_requires='>=3.7'
      )
