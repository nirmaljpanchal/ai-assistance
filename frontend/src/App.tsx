import { useState } from 'react'
import './App.css'

function App(): JSX.Element {
  const [count, setCount] = useState<number>(0)

  return (
    <div className="app">
      <div className="card">
        <button onClick={() => setCount((c) => c + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite logo to learn more
      </p>
    </div>
  )
}

export default App
