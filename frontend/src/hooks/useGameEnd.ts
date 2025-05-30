import { useEffect, useState, useRef } from "react";

import { useSocketContext } from "../contexts/socketContext";

type playAgainStatus = {
	O: string,
	X: string
}

type winnerInfo = {
	text: string,
	symbol: string
}

const useGameEnd: (
	setVisible: (visible: boolean) => void
) => [winnerInfo, playAgainStatus] = (setVisible) => {
	const { addMessageListener, removeMessageListener } = useSocketContext();

	const [playAgainState, setPlayAgainState] = useState<playAgainStatus>({
		O: '',
		X: '',
	});
	
	const winnerRef = useRef<winnerInfo>({ text: "", symbol: "" });

	useEffect(() => {
		const playAgainStateUpdateFn = (newState: {
			X: boolean | null;
			O: boolean | null;
		}) => {
			setPlayAgainState({
				X: newState.X === null ? '' : newState.X ? `\u2714` : `\u2717`,
				O: newState.O === null ? '' : newState.O ? `\u2714` : `\u2717`
			});
		}

		addMessageListener("play-again-state-update", playAgainStateUpdateFn, true);

		return () =>
			removeMessageListener("play-again-state-update", playAgainStateUpdateFn);
	}, [playAgainState]);

	useEffect(() => {
		const gameEndedFn = ({
			winner,
			symbol,
		}: {
			winner: boolean | string;
			symbol?: string | undefined;
		}) => {
			winnerRef.current = {
				text: symbol ? (winner ? "YOU WON!" : "YOU LOST!") : "TIE!", //TODO: test it
				symbol: symbol ? symbol : "O / X"
			}
			setVisible(true);
		}

		const restartGameFn = () => {
			setPlayAgainState({ O: '', X: '' });
			setVisible(false);
		}

		addMessageListener("game-ended", gameEndedFn);
		addMessageListener("game-restarted", restartGameFn);

		return () => {
			removeMessageListener("game-ended", gameEndedFn);
			removeMessageListener("game-restarted", restartGameFn);
		}
	}, [setVisible]);

	return [winnerRef.current, playAgainState];
}

export default useGameEnd;
