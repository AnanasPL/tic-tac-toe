import React from 'react';

interface CellProps {
  value: string,
  onClick: any
}

const Cell = ({ value, onClick }: CellProps) => {
  return (
    <div className='cell' onClick={onClick}>
      {value}
    </div>
  );
}

export default React.memo(Cell);