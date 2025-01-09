import React from 'react';

import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { socketContext } from '../contexts/socketContext';

import useSocket from '../hooks/useSocket';

import Rooms from './MainPage/Rooms';
import GamePage from './GamePage/GamePage';

import PageNotFound from './ErrorPages/PageNotFound';
import RoomNotFound from './ErrorPages/RoomNotFound';

import config from '../config.json';

const router = createBrowserRouter([
	{
		path: '/',
		element: <Rooms />,
		errorElement: <PageNotFound />,
	},
	{
		path: '/room/:roomCode',
		element: <GamePage />,
	},
	{
		path: '/room-not-found',
		element: <RoomNotFound />,
	},
],
	{
		basename: config.basename,
	}
);

const App = () => {
	const socket = useSocket();

	return (
		<socketContext.Provider value={socket}>
			<RouterProvider router={router} />
		</socketContext.Provider>
	);
}

export default App;