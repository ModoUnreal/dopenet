# DopeNet
This is just a joke website I'm making to learn more about flask,
take a look around if you want!

## Setting up
Get the source code using the following:

```bash
$ git clone https://www.github.com/ModoUnreal/dopenet.git
```

Once inside the dopenet directory you should probably set up a virtual environment:

```bash
$ virtualenv <env_name>
$ <env_name>\Scripts\activate
```

(Replace `env_name` with whatever you want to call it)

And then install all the necessary requirements using:

```bash
$ pip install -r requirements.txt
```

Set up FLASK_APP using the following:

```bash
$ set FLASK_APP=dopenet.py
```

Finally, you can run dopenet:

```bash
$ flask run
```

The website should be running in your local network, so probably `localhost:5000`.
