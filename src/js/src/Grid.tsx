import { Stage, Layer, Rect } from 'react-konva';
import { Cell } from './Cell';


const NUM_ROWS = 20;
const NUM_COLUMNS = 10;


export const Grid = ({grid}) => {
    const cellCoords = [];
    for (let row = 0; row < NUM_ROWS; row++) {
        for (let column = 0; column < NUM_COLUMNS; column++) {
            cellCoords.push([row, column]);
        }
    }
    return <Stage width={500} height={1000}>
        <Layer>
            {cellCoords.map(([row, column]) => <Cell
                row={row}
                column={column}
                status={grid[row][column].status}
            />)}
        </Layer>
    </Stage>
}