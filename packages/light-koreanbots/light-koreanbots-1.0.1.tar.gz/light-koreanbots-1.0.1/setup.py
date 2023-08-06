import setuptools

with open("README.md", "r", encoding="UTF-8") as f:
    long_description = f.read()

setuptools.setup(
    name="light-koreanbots",
    version="1.0.1",
    author="eunwoo1104",
    author_email="sions04@naver.com",
    description="(비공식) Koreanbots에 길드수 업데이트만 하는 모듈입니다.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eunwoo1104/light-koreanbots",
    packages=setuptools.find_packages(exclude=["example"]),
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
