export interface Conversa {
  id: string;
  numero: string;
  nome_contato?: string;
  text?: {
  message?: string;
};
  data_recebimento_servidor: string;
}