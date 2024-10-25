import React, { useContext, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';

import socketContext from '../../contexts/socketContext';

const AddRoom = () => {
	const { emit, addMessageListener, removeMessageListener } = useContext(socketContext);
	const navigate = useNavigate();
	
	useEffect(() => {
		const roomCreatedSuccessfullyFn = (code) => navigate(`/room/${code}`) //TODO: Full rooms

		addMessageListener('room-created-successfully', roomCreatedSuccessfullyFn, true);

		return () => removeMessageListener('room-created-successfully', roomCreatedSuccessfullyFn);
	}, []); 

	return (
		<div className='addRoom'>
			<button id='roomCreation' onClick={() => {
				emit('remove-empty-rooms');
				emit('create-room');
				}}>
				Create New Room
			</button>
		</div>
	);
};

export default AddRoom;