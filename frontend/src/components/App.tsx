import React from 'react';

import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { socketContext } from '@/contexts/socketContext';

import useSocket from '@/hooks/useSocket';

import Rooms from './RoomsView/Rooms';
import RoomPage from './RoomPage/RoomPage';

import ErrorPage from './errorPages/BasicErrorPage';
import RoomNotFound from './errorPages/RoomNotFound';

const router = createBrowserRouter([
	{
		path: '/',
		element: <Rooms />,
		errorElement: <ErrorPage />,
	},
	{
		path: '/room/:roomCode',
		element: <RoomPage />,
	},
	{
		path: '/room-not-found',
		element: <RoomNotFound />,
	},
]);

const App = () => {
	return (
		<socketContext.Provider value={useSocket()}>
			<RouterProvider router={router}></RouterProvider>
		</socketContext.Provider>
	);
}

export default App;