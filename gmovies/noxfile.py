import nox


@nox.session
def tests(session):
    session.run("pytest", external=True)


@nox.session
def lint(session):
    session.run("black", "gmovies", external=True)
    session.run("mypy", "gmovies", external=True)
    session.run("bandit", "-r", "gmovies", external=True)
    session.run("isort", "gmovies", external=True)
    session.run("autoflake", "--in-place", "--recursive", "--remove-all-unused-imports", "gmovies", external=True)
    session.run("flake8", "gmovies", external=True)
    session.run("pyupgrade", "--py311-plus", external=True)
