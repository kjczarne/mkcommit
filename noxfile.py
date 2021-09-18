import nox
import os
import shutil


@nox.session()
def test(session: nox.Session):
    """Run tests under coverage"""
    session.install(
        '.',
        'coverage'
    )
    session.run(
        'coverage', 'run', '-m', 'unittest', 'discover'
    )


@nox.session()
def cov(session: nox.Session):
    """Compile coverage to an XML file"""
    session.install('coverage')
    session.run('coverage', 'xml', '-i')


@nox.session
def lint(session: nox.Session):
    """Run the linter"""
    session.install('flake8')
    session.run('flake8')


@nox.session()
def whl(session: nox.Session):
    """Build the wheel"""
    session.install(
        'wheel',
        'setuptools',
        '.'
    )
    session.run('python', '-m', 'setup', 'bdist_wheel')


@nox.session()
def send(session: nox.Session):
    """Send wheel to PyPi"""
    session.install('twine')
    session.run('twine', 'upload', 'dist/*.whl')


@nox.session()
def clean(session: nox.Session):
    """Remove files that aren't needed anymore"""
    delete = [
        ".coverage",
        "build",
        "dist"
    ]
    for p in delete:
        if os.path.exists(p):
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
