# Contributing

Hello! Welcome and thank you for dedicating your time to make `pycaprio` even better.

Here are a few guidelines and "How to"s that will help you with the contribution.

## Before contributing...

Take a moment to search through `pycaprio`'s [issues](https://github.com/JavierLuna/pycaprio/issues) to check whether
the bug you are experiencing or the feature you would want implemented are being discussed.

Please check out the [Code of Conduct](https://github.com/JavierLuna/pycaprio/blob/main/CODE_OF_CONDUCT.md) for this
repository. This Code of Conduct is adapted from the Contributor Covenant, version 2.0, available
at http://contributor-covenant.org/version/2/0/code_of_conduct/

Lastly, please remember that I am a human as well. I will get back to you whenever I have time, be patient if I don't
reply in a couple of days or three.

## Pull requests

Once you are done with your contribution (don't forget about tests and documentation!), please open a pull request
against `main`.

Please, read ["How to write a Git commit message"](https://chris.beams.io/posts/git-commit/) before writing your commit
messages, I will expect the messages to follow that advise.

Include a reference to the open related issue and wait for me to review the changes and for the CI to run the
tests/linting.

Further code discussion should go in the Pull Request, while the rest should go into the issue.

Once the PR is approved, I'll merge the PR and schedule it for a next release.

## How to work on Pycaprio

### Setup your workplace

Fork the repository into your account and clone it in your work station.

To work on `pycaprio`, you will need Python 3.6+ and [Poetry](https://github.com/python-poetry/poetry) installed.

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

For the integration tests, you will need a reachable INCEpTION instance that has the remote API enabled. Needlessly to
say, **DO NOT USE A PROD INSTANCE FOR THIS, USE A DISPOSABLE ONE**. By default, the integs will
target `http://localhost:8080`, although you can override that value via `TEST_INCEPTION_ENDPOINT` env variable.

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

