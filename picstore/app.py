from picstore import cli


def start() -> None:
    arguments = cli.parse()
    command_to_run = vars(arguments).pop("command")
    for command in cli.all_commands:
        if command_to_run == command.name:
            command.run(arguments=arguments)
            break
