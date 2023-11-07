from picstore import picstore


# TODO: final (manual) test of every command
# TODO: improve speed:
# TODO: --> ONLY EVER use pictype module call for multiple files (maybe remove single file methods)
# TODO: --> load picdirs and maybe picdir content on demand and not all at once at start


def main():
    picstore.start()


if __name__ == "__main__":
    main()
