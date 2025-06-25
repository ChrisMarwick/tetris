import { Layer, Rect } from "react-konva"
import { CANVAS_WIDTH, CANVAS_HEIGHT } from '../config';
import { CanvasButton } from "./CanvasButton";


const PADDING = 125;


interface HighScoreProps {
    onClose: () => void;
}


export const HighScore = ({onClose}: HighScoreProps) => {
    return <Layer>
        <Rect
            x={PADDING}
            y={PADDING}
            width={CANVAS_WIDTH - 2 * PADDING}
            height={CANVAS_HEIGHT - 2 * PADDING}
            cornerRadius={10}
            fill='black'
        />
        <CanvasButton
            text='Close'
            x={PADDING + 30}
            y={CANVAS_HEIGHT - PADDING - 60}
            width={70}
            height={35}
            onClick={onClose}
            invertedColors
        />
    </Layer>
}