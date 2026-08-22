import PeerGroupDisplay from "./PeerGroupDisplay";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>EduConnect</h1>
        <p>Peer-Group Formation System</p>
      </header>

      <main>
        <PeerGroupDisplay />
      </main>
    </div>
  );
}

export default App;
