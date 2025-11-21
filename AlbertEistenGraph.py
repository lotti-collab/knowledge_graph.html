import os
import asyncio
from pyvis.network import Network
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from dotenv import load_dotenv
load_dotenv()

# load .env if present
load_dotenv()

# ----------------------------------------
# CONFIGURE O MODELO (melhor: via variável de ambiente)
# ----------------------------------------
API_KEY = os.getenv("OPENAI_API_KEY")  # ← AGORA CERTO

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY não definida. Use setx ou um .env com OPENAI_API_KEY.")

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=API_KEY
)
graph_transformer = LLMGraphTransformer(llm=llm)


# ----------------------------------------
# FUNÇÃO 1 — Extração do Grafo
# ----------------------------------------
async def extract_graph_data(text):
    """
    Extrai entidades e relações do texto usando LLMGraphTransformer.
    """
    docs = [Document(page_content=text)]
    graph_documents = await graph_transformer.aconvert_to_graph_documents(docs)
    return graph_documents


# ----------------------------------------
# FUNÇÃO 2 — Visualização com PyVis
# ----------------------------------------
def visualize_graph(graph_documents):
    net = Network(
        height="1200px",
        width="100%",
        directed=True,
        notebook=False,
        bgcolor="#222222",
        font_color="white",
        filter_menu=True,
        cdn_resources='remote'
    )

    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    node_dict = {node.id: node for node in nodes}

    valid_edges = []
    valid_node_ids = set()

    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])

    for node_id in valid_node_ids:
        node = node_dict[node_id]
        net.add_node(node.id, label=node.id, title=node.type, group=node.type)

    for rel in valid_edges:
        net.add_edge(rel.source.id, rel.target.id, label=rel.type.lower())

    net.set_options("""
        {
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -100,
                    "centralGravity": 0.01,
                    "springLength": 200,
                    "springConstant": 0.08
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
    """)

    output_file = "knowledge_graph.html"
    net.save_graph(output_file)
    print(f"Graph saved to: {os.path.abspath(output_file)}")
    return net


# ----------------------------------------
# FUNÇÃO 3 — Pipeline Completo
# ----------------------------------------
def generate_knowledge_graph(text):
    graph_documents = asyncio.run(extract_graph_data(text))
    net = visualize_graph(graph_documents)

    # Salva sem abrir (fix do PyVis)
    net.save_graph("knowledge_graph.html")
    print("Arquivo gerado: knowledge_graph.html — abra manualmente no navegador.")

    return net


# ----------------------------------------
# EXECUTAR O SCRIPT DIRETO
# ----------------------------------------
if __name__ == "__main__":
    texto = """Albert Einstein[a] (Ulm, 14 de março de 1879 – Princeton, 18 de abril de 1955) foi um físico teórico alemão que desenvolveu a teoria da relatividade geral, um dos pilares da física moderna ao lado da mecânica quântica. Embora mais conhecido por sua fórmula de equivalência massa–energia, E = mc² — que foi chamada de "a equação mais famosa do mundo" —, foi laureado com o Prêmio Nobel de Física de 1921 "por suas contribuições à física teórica" e, especialmente, por sua descoberta da lei do efeito fotoelétrico, que foi fundamental no estabelecimento da teoria quântica.

Nascido em uma família de judeus alemães, mudou-se para a Suíça ainda jovem e iniciou seus estudos na Escola Politécnica de Zurique. Após dois anos procurando emprego, obteve um cargo no escritório de patentes suíço enquanto ingressava no curso de doutorado da Universidade de Zurique. Em 1905, publicou uma série de artigos acadêmicos revolucionários. Uma de suas obras era o desenvolvimento da teoria da relatividade especial. Percebeu, no entanto, que o princípio da relatividade também poderia ser estendido para campos gravitacionais, e com a sua posterior teoria da gravitação, de 1916, publicou um artigo sobre a teoria da relatividade geral. Enquanto acumulava cargos em universidades e instituições, continuou a lidar com problemas da mecânica estatística e teoria quântica, o que levou às suas explicações sobre a teoria das partículas e o movimento browniano. Também investigou as propriedades térmicas da luz, o que lançou as bases da teoria dos fótons. Em 1917, aplicou a teoria da relatividade geral para modelar a estrutura do universo como um todo. Suas obras renderam-lhe o status de celebridade mundial enquanto tornava-se uma nova figura na história da humanidade, recebendo prêmios internacionais e sendo convidado de chefes de estado e autoridades. Foi professor da Academia de Ciências de Berlim.

Em 1933, quando o Partido Nazista chegou ao poder na Alemanha, estava nos Estados Unidos, onde passou a morar. Desde então, não tornou a residir no seu país de origem. Naturalizou-se estadunidense em 1940. Em agosto de 1939, pouco antes da eclosão da Segunda Guerra Mundial,[5] ajudou a alertar o presidente Franklin D. Roosevelt que a Alemanha poderia estar desenvolvendo uma arma atômica, recomendando aos norte-americanos começarem uma pesquisa semelhante, que se tornaria o Projeto Manhattan. Apoiou os Aliados,[6] opondo-se, no entanto, à utilização de armas nucleares contra o Japão.[5] Mais tarde, com o filósofo britânico Bertrand Russell, assinou o Manifesto Russell-Einstein, que destacou o perigo das armas nucleares. Foi afiliado ao Instituto de Estudos Avançados de Princeton, onde trabalhou até sua morte em 1955.

Realizou diversas viagens ao redor do mundo, deu palestras públicas em conceituadas universidades e conheceu personalidades célebres de sua época, tanto na ciência quanto fora do mundo acadêmico. Publicou mais de 300 trabalhos científicos, juntamente com mais de 150 obras não científicas. Suas grandes conquistas intelectuais e originalidade fizeram da palavra "Einstein" sinônimo de gênio. Em 1999, foi eleito por 100 físicos renomados o mais memorável físico de todos os tempos. No mesmo ano, a revista TIME, em uma compilação com as pessoas mais importantes e influentes, classificou-o a pessoa do século XX."""  
    print("Gerando grafo...")
    generate_knowledge_graph(texto)
    print("Pronto! Abra knowledge_graph.html")