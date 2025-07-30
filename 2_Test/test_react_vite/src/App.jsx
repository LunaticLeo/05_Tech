import { useState } from 'react';
import reactLogo from './assets/react.svg';
import './App.css';
import { useEffect } from 'react';

function App() {
	const [a, setA] = useState(0);
	const [b, setB] = useState(0);
	const [sum, setSum] = useState(0);

	useEffect(() => {
		setSum(a + b);
	}, [a, b]);

	return (
		<div className='App'>
			<input value={a} onChange={e => setA(Number(e.target.value))} />
			<input value={b} onChange={e => setB(Number(e.target.value))} />
			<p>{sum}</p>
		</div>
	);
}

export default App;
