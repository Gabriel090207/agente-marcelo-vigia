import { useEffect, useState } from "react";
import axios from "axios";
import type { Conversa } from "./types/Conversa";
import Painel from "./components/painel";
import "./styles/global.css";
import "./styles/layout.css";

function App() {
  const [conversas, setConversas] = useState<Conversa[]>([]);

  useEffect(() => {
    axios
      .get("https://agente-marcelo-vigia.onrender.com/api/conversas")
      .then((res) => setConversas(res.data));
  }, []);

  return (
    <Painel conversas={conversas} />
  );
}

export default App;