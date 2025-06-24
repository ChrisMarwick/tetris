import { Layer } from 'react-konva';
import { Cell } from './Cell';
import { ICell } from '../interfaces/cell';
import { NUM_COLUMNS, NUM_ROWS } from '../config';


interface GridProps {
    grid: Record<number, Record<number, ICell>>
}


export const Grid = ({grid}: GridProps) => {
    const cellCoords = [];
    for (let row = 0; row < NUM_ROWS; row++) {
        for (let column = 0; column < NUM_COLUMNS; column++) {
            cellCoords.push([row, column]);
        }
    }
    return <Layer>
        {cellCoords.map(([row, column]) => <Cell
            key={`${row}-${column}`}
            row={row}
            column={column}
            status={grid ? grid[row][column].status : 'EMPTY'}
            color={grid ? grid[row][column].color : 'black'}
        />)}
    </Layer>
}