from setuptools import setup

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(name='gym_prismata',
    version='0.1',
    install_requires=['gym','prismataengine'],
       description = 'OpenAI Gym environment for Dave Churchill\'s turn-based strategy game Prismata',
       author="Shauna Kravec",
       author_email="smkravec@celest.ai",
       long_description=long_description,
       long_description_content_type="text/markdown",
       url="https://github.com/smkravec/gym-prismata",
       classifiers=[
           "Programming Language :: Python :: 3",
           "Operating System :: OS Independent",
           ],
       python_requires='>=3.6',
)
