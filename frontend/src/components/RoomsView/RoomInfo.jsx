import React from "react";
import { useNavigate } from 'react-router-dom' 

const Room = ({ code, size }) => {
	const navigate = useNavigate()

	const getColor = () => {
		return size === 0 ? 'green' : size === 1 ? 'yellow' : 'red'
	}

	return <div className={`room ${getColor()}`} onClick={() => navigate(`/room/${code}`)}>{code}</div>;
};

export default Room;
