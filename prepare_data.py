from llama_index.core import Settings
from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.llms.llamafile import Llamafile
from llama_index.core.node_parser import SentenceSplitter

Settings.embed_model = LlamafileEmbedding(base_url="http://localhost:8080")

Settings.llm = Llamafile(
	base_url="http://localhost:8080",
	temperature=0,
	seed=0
)

# Also set up a sentence splitter to ensure texts are broken into semantically-meaningful chunks (sentences) that don't take up the model's entire
# context window (2048 tokens). Since these chunks will be added to LLM prompts as part of the RAG process, we want to leave plenty of space for both
# the system prompt and the user's actual question.
Settings.transformations = [
	SentenceSplitter(
    	chunk_size=256,
    	chunk_overlap=5
	)
]

# Load local data
from llama_index.core import SimpleDirectoryReader
local_doc_reader = SimpleDirectoryReader(input_dir='./data')
docs = local_doc_reader.load_data(show_progress=True)

# We'll load some Wikipedia pages as well
# from llama_index.readers.web import SimpleWebPageReader
# urls = [
# 	'https://www.ato.gov.au/law/view/document?LocID=%22TXD%2FTD201221%2FNAT%2FATO%22&PiT=20240920000000',
# ]
# web_reader = SimpleWebPageReader(html_to_text=True)
# docs.extend(web_reader.load_data(urls))

# Build the index
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(
	docs,
	show_progress=True,
	streaming=True,
)

# Save the index
index.storage_context.persist(persist_dir="./storage")

query_engine = index.as_query_engine()
print(query_engine.query("if I remove a potential beneficiary of a discretionary trust will that trigger a resettlement for the purposes of capital gains tax?"))
