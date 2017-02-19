from .cli import cli


_CLI_NAME = 'dkron-cli'


def main(args=None):
    cli(prog_name=_CLI_NAME)


if __name__ == "__main__":
    main()
