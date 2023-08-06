from wafec.fi.hypothesis.models._base import Base, engine


if __name__ == '__main__':
    Base.metadata.create_all(engine)
