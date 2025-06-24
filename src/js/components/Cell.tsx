import { Rect } from 'react-konva';
import { CELL_SIZE } from '../config';


const CELL_BORDER_WIDTH = 1;


interface CellProps {
    row: number;
    column: number;
    status: string;
    color: string;
}


export const Cell = ({row, column, status, color}: CellProps) => {
    return <Rect 
        key={`key-${column}-${row}`}
        x={column * CELL_SIZE} 
        y={row * CELL_SIZE} 
        width={CELL_SIZE} 
        height={CELL_SIZE} 
        fill={color}
        stroke='white' 
        strokeWidth={CELL_BORDER_WIDTH}
    />
}