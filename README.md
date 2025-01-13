# An online Tic-tac-toe multiplayer game

[LIVE DEMO](https://ananaspl.github.io/tic-tac-toe)

## About

### Technology used:

- **Python** for backend (**Flask**)
- **React** for frontend (**TypeScript**) 
- **Sass** for styling
- **FlaskSocketIO** and **Socket.IO** for client - server communication
- **Pytest** and **Playwright** for testing

### Features:

 - Real-time online Tic-tac-toe game
 - Multiple rooms allowing multiple games at the same time
 - Rejoining* (if one or both players leave, the game can be continued)
 - Playing again after the game is finished, with the change of the symbols
 - *Playing against the AI***
 - *Custom themes and symbols***
 - *Custom room names***
 - *Spectating games***
 - *Rooms with password***

\* --- works, but can be bugged in very specific cases \
** --- planned; may or may not be implemented

## Installing locally

The game can be played online (link at the top), but can also be installed locally to play on your LAN, host your own game server or just test and have fun with the code.

### 1. Clone the repository
```
git clone https://github.com/AnanasPL/tic-tac-toe.git
```
### 2. Install Python modules

The code was written on Python 3.9,10 and should work on every newer version. Older 3.0+ versions should, but might not work properly.
 
#### a. Create virtual environment
In the `/backend/` directory:
```
python -m venv venv
```
#### b. Activate virtual environment

On Windows:
```
./venv/Scripts/activate.bat
```
On MacOS and Linux:
```
source ./venv/bin/activate
```
\
In case of any trouble activating the environment visit [this site](https://docs.python.org/3/library/venv.html#how-venvs-work).
#### c. Install the modules
```
pip install -r ./requirements.txt
```
### 3. Install Node modules
In the `/frontend/` directory run:
```
npm install --legacy-peer-deps
```
Or if you're using yarn:
```
yarn install --ignore-peer-deps
```
### 4. Configure to run locally

You can customize the configuration to run the app locally: 
\
In the `/backend/config.json`, `host` specifies the host of your app. You can change it to `127.0.0.1` to make it accessible from your machine only. `port` specifies the port that the app will run on. `CORS_allowed_origins` is a list of origins, that the server should accept requests from. 

In the `/frontend/src/config.json`, `socket_url` specifies the url that socket requests will be sent to. `basename` specifies the prefix of every url in the app. For example, if basename is set to  `spaghetti`, the app will be accessible at `http(s)://<HOST_ADDRESS>/spaghetti/` instead of `http(s)://<HOST_ADDRESS>/`, which would be when basename is left blank.

#### Example configuration:
`/backend/config.json`: 
 ```
{
	"host": "127.0.0.1",
	"port": 5000,
	"CORS_allowed_origins": [
		"http://localhost:3000",
		"http://127.0.0.1:3000"
	]
}
```

`/frontend/src/config.json`:
```
{
	"socket_url": "http://localhost:5000",
	"basename": ""
}
```
