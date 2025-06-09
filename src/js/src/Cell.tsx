import { useMemo } from 'react';
import { Rect } from 'react-konva';


const CELL_SIZE = 50;
const CELL_BORDER_WIDTH = 1;


export const Cell = ({row, column, status}) => {
    const cellColor = useMemo(() => {
        switch (status) {
            case 'EMPTY':
                return 'white';
            case 'VISITED':
                return 'yellow';
            case 'OCCUPIED':
                return 'red';
            default:
                throw `Unknown status ${status}`
        }
    }, [status]);

    return <Rect 
        key={`key-${column}-${row}`}
        x={column * CELL_SIZE} 
        y={row * CELL_SIZE} 
        width={CELL_SIZE} 
        height={CELL_SIZE} 
        fill={cellColor}
        stroke='black' 
        strokeWidth={CELL_BORDER_WIDTH}
    />
}