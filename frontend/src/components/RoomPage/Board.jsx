import React, { useEffect, useContext } from 'react';

import { useParams } from 'react-router-dom';

import socketContext from '../../contexts/socketContext';

import useBoardState from '../../hooks/useBoardState';

import Cell from './Cell';
import WinnerInfo from './WinnerInfo';

const Board = () => {
  const { emit } = useContext(socketContext);
  const boardState = useBoardState();
  const { roomCode } = useParams();

  useEffect(() => {
    emit('join-room', roomCode);

    return () => emit('leave-room', roomCode);
  }, []);

  return (
    <div className='board'>
      {boardState.map((val, id) => 
        <Cell 
        value={val} 
        onClick={() => emit('board-update', id)}
        key={id}/>)}
      <WinnerInfo />
    </div>
  );
};

export default Board;