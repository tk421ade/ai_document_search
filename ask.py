from llama_index.core import StorageContext
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core import (
    load_index_from_storage,
    load_indices_from_storage,
    load_graph_from_storage,
)
from llama_index.core import Settings
from llama_index.embeddings.llamafile import LlamafileEmbedding
from llama_index.llms.llamafile import Llamafile

Settings.embed_model = LlamafileEmbedding(base_url="http://localhost:8080")

Settings.llm = Llamafile(
    base_url="http://localhost:8080",
    temperature=0,
    seed=0
)


storage_dir = "./storage"

storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir=storage_dir),
    vector_store=SimpleVectorStore.from_persist_dir(
        persist_dir=storage_dir
    ),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir=storage_dir),
)
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
print(query_engine.query("if I remove a potential beneficiary of a discretionary trust will that trigger a resettlement for the purposes of capital gains tax?"))


