# Contributing

Please refer to the [DKPro Contribution Guidelines](https://dkpro.github.io/contributing) that govern all subprojects of INCEpTION.

## How to work on Pycaprio

### Setup your workplace

Fork the repository into your account and clone it in your work station.

To work on `pycaprio`, you will need Python 3.8+ and [Poetry](https://github.com/python-poetry/poetry) installed.

There's a [Makefile](https://github.com/JavierLuna/pycaprio/blob/main/Makefile) to make your dev life easier, but if you
cannot run `make` in your system, just open the file and do the same commands.

### Installing the dependencies

Now, you have two options (this is just up to personal preference):

1. Create and manage your own virtual env, activate it and develop inside it.
   Read [this](https://realpython.com/python-virtual-environments-a-primer/).
2. Let Poetry handle virtual environments for you. Then just use the `make`.

I personally prefer option **1** but feel free to use whichever is more comfortable to you.

Once you are ready, just do `make dependencies` and that will install both dev and prod dependencies.

At this point, you should have everything ready to start developing, but what is developing without tests...

### Run tests and the linter

This project has both unit tests and integration tests. Unit tests are fine to run in isolation by
just `make unit-tests`.

You will need to then create an user there and enable `REMOTE_API` permissions.

The username and password should be `test-remote`, although you can override those values by using the
`TEST_USERNAME` and `TEST_PASSWORD` env variables.

To run the integration tests use: `make integ-tests`

To run all tests use: `make tests`

To run the linter: `make lint`

### Documentation

There's a [docs](https://github.com/JavierLuna/pycaprio/tree/main/docs) directory that contains all `pycaprio`'s
documentation.

You may add/change the files there if your contribution requires so.

To compile the documentation and serve them in a local webserver, do `make docs`.

