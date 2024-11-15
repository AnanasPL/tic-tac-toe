import React from 'react';

import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { socketContext } from '../contexts/socketContext';

import useSocket from '../hooks/useSocket';

import Rooms from './RoomsPage/Rooms';
import GamePage from './GamePage/GamePage';

import ErrorPage from './ErrorPages/BasicErrorPage';
import RoomNotFound from './ErrorPages/RoomNotFound';

const router = createBrowserRouter([
	{
		path: '/',
		element: <Rooms />,
		errorElement: <ErrorPage />,
	},
	{
		path: '/room/:roomCode',
		element: <GamePage />,
	},
	{
		path: '/room-not-found',
		element: <RoomNotFound />,
	},
]);

const App = () => {
	const socket = useSocket();

	return (
		<socketContext.Provider value={socket}>
			<RouterProvider router={router} />
		</socketContext.Provider>
	);
}

export default App;