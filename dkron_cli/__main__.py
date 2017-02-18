from .cli import cli


_ME = 'dkron-cli'


def main(args=None):
    cli(prog_name=_ME)


if __name__ == "__main__":
    main()
