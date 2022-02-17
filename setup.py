from setuptools import setup,find_packages
setup(
    name="gamegui",
    version="1.3.1",
    description="A widget-based pygame GUI Framework",
    long_description="""\
This is a widget-based pygame GUI framework.
Due to my limited time(this is a 1-person project),
I can't write a tutorial to use this framework.
However, you can visit the "demos" folder to learn
how to use this framework.

If you want to contribute to this project, send
me an email(at Programmer00001H@gmail.com).

Any help/contributions are appreciated.""".replace("\n"," "),
    long_description_content_type="text/plain",
    url="https://github.com/00001H/GameGui",
    author="00001H",
    author_email="Programmer00001H@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: User Interfaces"
    ],
    packages=find_packages(where="."),
    python_requires=">=3.8, <4",
    install_requires=["pygame","pyperclip"],
    project_urls={
        "Bug Reports":"https://github.com/00001H/GameGui/issues",
        "Source Code":"https://github.com/00001H/GameGui"
    }
)
