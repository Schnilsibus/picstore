from picstore import app


# TODO: improve speed:
# TODO: --> ONLY EVER use pictype module call for multiple files (maybe remove single file methods)
# TODO: --> load picdirs and maybe picdir content on demand and not all at once at start
# TODO: Battle the duplicate --> use logging --> while doing so make nicer output to user
# TODO: make it buildable with new setuptools syntax (setup.cfg files etc.)

def main():
    app.start()


if __name__ == "__main__":
    main()
