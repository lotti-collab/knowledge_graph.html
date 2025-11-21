🧠 Knowledge Graph Generator (LLM + Python + PyVis)

Este projeto gera grafo de conhecimento automaticamente a partir de qualquer texto usando:

LangChain + LLMGraphTransformer

OpenAI GPT-4o-mini

PyVis para visualização interativa

Extração assíncrona de entidades e relações

Interface HTML para explorar o grafo

🚀 Funcionalidades

✔️ Extrai entidades automaticamente de qualquer texto
✔️ Identifica relações entre entidades
✔️ Gera um grafo navegável em HTML
✔️ Permite reutilizar o pipeline com qualquer fonte de dados
✔️ Ideal para IA, NLP, Pesquisa, Estudos, Automação e Data Science

Instalacao

git clone https://github.com/lotti-collab/knowledge_graph.html.git
cd knowledge_graph.html
pip install -r requirements.txt


🔑 Configuração da OpenAI API Key
Crie um arquivo .env na raiz do projeto:

ini
Copiar código
OPENAI_API_KEY=coloque_sua_chave_aqui

▶️ Execução
python AlbertEistenGraph.py

O grafo será salvo como:
knowledge_graph.html

📊 Exemplo de saída

Grafo gerado a partir da biografia de Albert Einstein:

🔗 knowledge_graph.html (interativo e navegável)

🤝 Contribuições

Sinta-se à vontade para abrir Issues, enviar PRs ou sugerir melhorias.

📄 Licença

MIT.
