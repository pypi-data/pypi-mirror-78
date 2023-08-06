from setuptools import setup

README = open("README.md","r").read()
setup(
    name="BonziBuddy",
    version='1.0',
    description="A Smaller Version Of Great BonziBuddy In Pure Python..",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/BLUE-DEVIL1134/BonziBuddy",
    author="Akash Pattnaik",
    author_email="akashpattnaik.github@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=["BonziBuddy"],
    install_requires=['pyttsx3','wikipedia','pyTelegramBotAPI==3.6.6'],
    entry_points={
        "console_scripts": [
            "Bonzi=BonziBuddy.__init__:start",
            "BonziBuddy=BonziBuddy.__init__:start",
            "bonzi=BonziBuddy.__init__:start",
        ]
    },
)
