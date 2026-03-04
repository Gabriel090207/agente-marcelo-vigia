import type { Conversa } from "../types/Conversa";
import "../styles/painel.css";

interface Props {
  conversas: Conversa[];
}

export default function Painel({ conversas }: Props) {
  return (
    <div className="painel-container">
      <header className="painel-header">
        <h1>Painel de Conversas</h1>
      </header>

      <div className="cards-container">
        {conversas.map((c) => (
  <div key={c.id} className="card">
    <h3>{c.nome_contato || "Sem nome"}</h3>
    <p>{c.numero}</p>

    <p className="data-msg">
      {c.data_recebimento_servidor
        ? new Date(c.data_recebimento_servidor).toLocaleString("pt-BR")
        : "Sem data"}
    </p>
  </div>
))}
      </div>
    </div>
  );
}