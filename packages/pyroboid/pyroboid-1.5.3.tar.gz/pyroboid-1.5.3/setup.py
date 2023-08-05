from setuptools import setup, find_packages

setup(
	name="pyroboid",
	version="1.5.3",
	author="Kwang-Hyun Park",
	author_email="akaii@kw.ac.kr",
	description="Python Package for Hamster, Hamster-S, Turtle, and Albert Ai",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/hamsterschool/pyroboid",
	install_requires=["pyserial"],
	packages=find_packages(exclude=["examples", "tests"]),
	python_requires=">=3",
	zip_safe=False,
	classifiers=[
		"License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
	]
)