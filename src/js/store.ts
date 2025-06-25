import { create } from "zustand";
import { IGrid } from "./interfaces/grid";


interface GameStoreData {
    grid: IGrid | null;
    score: number;
    level: number;
    game_state: 'IN_PROGRESS' | 'PAUSED' | 'ENDED';
}

interface IGameStore extends GameStoreData {
    update: (data: GameStoreData) => void;
}


export const useGameStore = create<IGameStore>((set) => ({
    grid: null,
    score: 0,
    level: 1,
    game_state: 'PAUSED',
    update: (data) => set(data)
}))
