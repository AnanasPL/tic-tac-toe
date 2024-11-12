import { createRoot } from 'react-dom/client';
import App from './components/App';

import './styles/style1.css';

const rootElement = createRoot(document.getElementById('root')!);
rootElement.render(<App />);