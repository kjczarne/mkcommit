import nox


@nox.session()
def test(session: nox.Session):
    pass


@nox.session
def lint(session: nox.Session):
    session.install('flake8')
    session.run()


@nox.session()
def docs(session: nox.Session):
    pass


@nox.session()
def wheel(session: nox.Session):
    pass


@nox.session()
def send(session: nox.Session):
    pass


@nox.session()
def clean(session: nox.Session):
    pass
