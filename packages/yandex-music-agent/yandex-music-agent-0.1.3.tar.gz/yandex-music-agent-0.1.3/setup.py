from setuptools import setup

setup(
    name="yandex-music-agent",
    version="0.1.3",
    description="Download yandex account favorites artists music",
    url="https://bitbucket.org/shmyga/yandex.music.agent",
    author="shmyga",
    author_email="shmyga.z@gmail.com",
    license="MIT",
    package_dir={"": "src"},
    packages=["yandex_music_agent", "yandex_music_agent.common"],
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "argparse",
        "aiohttp",
        "aiofiles",
        "aiostream",
        "beautifulsoup4",
        "lxml",
        "brotlipy",
        "mutagen",
        "asynctest",
    ],
    entry_points={
        "console_scripts": ["yandex-music-agent=yandex_music_agent.main:main"],
    }
)
