import React, { useEffect } from 'react';

import { useNavigate } from 'react-router-dom';

import { useSocketContext } from '../../contexts/socketContext';

const AddRoom = () => {
	const { emit, addMessageListener, removeMessageListener } = useSocketContext();
	const navigate = useNavigate();
	
	useEffect(() => {
		const roomCreatedSuccessfullyFn = (code: string) => navigate(`/room/${code}`) //TODO: Full rooms

		addMessageListener('room-created-successfully', roomCreatedSuccessfullyFn, true);

		return () => removeMessageListener('room-created-successfully', roomCreatedSuccessfullyFn);
	}, [navigate]); 

	return (
		<div className='add-room-button'>
			<button id='roomCreation' onClick={() => {
				emit('remove-empty-rooms');
				emit('create-room');
				}}>
				Create New Room
			</button>
		</div>
	);
}

export default AddRoom;