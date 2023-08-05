try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


def main():
    version = "0.3.3"
    setup(
        version=version,
        py_modules=["functiontrace"],
        ext_modules=[
            Extension(
                "_functiontrace",
                ["_functiontrace.c", "mpack/mpack.c"],
                extra_compile_args=["-std=c11"],
                define_macros=[("PACKAGE_VERSION", '"{}"'.format(version))],
            )
        ],
        entry_points={"console_scripts": ["functiontrace=functiontrace:main"]},
    )


if __name__ == "__main__":
    main()
