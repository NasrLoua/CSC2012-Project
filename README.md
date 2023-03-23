# CSC2012-Project

## Recycling Web Application

This is a web application that uses computer vision to identify an image and awards points to the user for correctly taking a photo of a recyclable item. It is developed in Python using Flask and Tensorflow. The project's database is created using MongoDB.

## Installation

Without Docker:

1. Clone the repository:

```
https://github.com/NasrLoua/CSC2012-Project.git
```

2. Install the requirements:

```
cd flask
pip3 install -r requirements.txt
```

With Docker:

1. Clone the repository:

```
https://github.com/NasrLoua/CSC2012-Project.git
```

## Usage

Without Docker:

1. Start the application:

```
python main.py
```

2. Open your web browser and go to `http://localhost:5001`
3. Register an account or log into the application using the following credentials:

```
User Test 1
username: test1
password: test1!

User Test 2
username: test2
password: test2!
```

With Docker:

1. Start the application:

```
$ docker compose up -d
```

2. After the application starts, navigate to http://localhost:80 in your web browser or run:

3. Stop and remove the containers:

```
$ docker compose down
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/NasrLoua/CSC2012-Project/LICENSE.md) file for details.
