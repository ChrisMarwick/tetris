import { CanvasButton } from "./CanvasButton";
import { Overlay, SIZE_X, SIZE_Y } from "./Overlay";
import { Rect, Text } from "react-konva";


const PADDING_X = 10;
const PADDING_Y = 30;


interface MenuProps {
    onClickNewGame: () => void;
    onClickHighScore: () => void;
}


export const Menu = ({onClickNewGame, onClickHighScore}: MenuProps) => {
    return <Overlay>
        <CanvasButton
            x={PADDING_X}
            y={PADDING_Y}
            width={(SIZE_X / 2) - (2 * PADDING_X)}
            height={SIZE_Y - (2 * PADDING_Y)}
            text="New Game"
            onClick={onClickNewGame}
        />
        <CanvasButton
            x={(SIZE_X / 2) + PADDING_X}
            y={PADDING_Y}
            width={(SIZE_X / 2) - (2 * PADDING_X)}
            height={SIZE_Y - (2 * PADDING_Y)}
            text="High Score"
            onClick={onClickHighScore}
        />
    </Overlay>
}