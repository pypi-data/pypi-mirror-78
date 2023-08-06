from wafec.fi.hypothesis.models._base import Base, engine


def main(args=None):
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
