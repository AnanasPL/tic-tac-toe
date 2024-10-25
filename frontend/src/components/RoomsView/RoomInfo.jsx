import React from 'react';

import { useNavigate } from 'react-router-dom' ;

const Room = ({ code, size }) => {
	const navigate = useNavigate();

	const getColor = () => {
		return size === 0 ? 'green' : size === 1 ? 'yellow' : 'red';
	};

	//TODO: Full rooms message showing
	return (
		<div className={`room ${getColor()}`} onClick={() => size !== 2 ? navigate(`/room/${code}`) : null}> 
			{code}
		</div>
	);
};

export default Room;