import { createRoot } from 'react-dom/client'
import App from './components/App'
import './styles/style.css'

const rootElement = createRoot(document.getElementById('root'))
rootElement.render(<App />)