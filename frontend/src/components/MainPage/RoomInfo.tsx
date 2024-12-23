import React from 'react';
import { useNavigate } from 'react-router-dom' ;

interface RoomProps {
	code: string,
	size: number
}

const Room = ({ code, size }: RoomProps) => {
	const navigate = useNavigate();

	return (
		<div className='room' onClick={() => size !== 2 ? navigate(`/room/${code}`) : null}> 
			{code}
			<div className='number-of-players' data-number-of-players={size}>
				{size}/2
			</div>
		</div>
	);
}

export default Room;