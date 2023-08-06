from wafec.fi.hypothesis.models._base import Base, engine


def run():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    run()
