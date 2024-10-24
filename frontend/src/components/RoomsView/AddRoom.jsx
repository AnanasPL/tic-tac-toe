import React, { useContext, useEffect } from 'react';

import { useNavigate } from 'react-router-dom';

import socketContext from '../../contexts/socketContext';

const AddRoom = () => {
	const { emit, addMessageListener } = useContext(socketContext);
	const navigate = useNavigate();
	
	useEffect(() => {
		addMessageListener('room-created-successfully', ({ code }) => {
			navigate(`/room/${code}`); //TODO: Full rooms
		}, true);
	}, []); 

	return (
		<div className='addRoom'>
			<button id='roomCreation' onClick={() => emit('create-room')}>
				Create New Room
			</button>
			<button onClick={() => emit('remove-empty-rooms')}>
				Clear rooms
			</button>
		</div>
	);
};

export default AddRoom;