import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="raindancesvi",
	version="0.1.0",
	author="Prasanth Shyamsundar",
	author_email="prasanth.s.cmi@gmail.com",
	description="A machine learning package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://prasanthcakewalk.gitlab.io/raindancesvi",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		'Development Status :: 3 - Alpha',
	],
	python_requires='>=3.6',
	license='MIT',
	keywords="machine learning rd6 inclass raindances",
	platforms=['any'],
	install_requires=['tensorflow>=2', 'numpy']
)
