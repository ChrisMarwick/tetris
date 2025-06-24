import { useMemo, useState, useEffect } from "react";
import { Layer, Rect, Text } from 'react-konva';
import classNames from "classnames";
import { INFO_BAR_HEIGHT, INFO_BAR_WIDTH, INFO_BAR_X } from "../config";


const PADDING = 20;


interface InfoBarProps {
    score: number;
    level: number;
}


export const InfoBar = ({score, level=0}: InfoBarProps) => {
    const scoreText = useMemo(() => `Score: ${score}`, [score]);
    const levelText = useMemo(() => `Level: ${level}`, [level]);

    return <Layer>
        <Rect
            x={INFO_BAR_X}
            width={INFO_BAR_WIDTH}
            height={INFO_BAR_HEIGHT}
            fill='black'
        />
        <Rect
            x={INFO_BAR_X + PADDING}
            y={PADDING}
            width={INFO_BAR_WIDTH - (2 * PADDING)}
            height={75}
            fill='white'
        />
        <Text
            x={INFO_BAR_X + (2 * PADDING)}
            y={2 * PADDING}
            fontSize={16}
            text={scoreText}
        />
        <Text
            x={INFO_BAR_X + (2 * PADDING)}
            y={(2 * PADDING) + 20}
            fontSize={16}
            text={levelText}
        />
    </Layer>
}
