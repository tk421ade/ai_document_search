clean:
	rm -rf venv
	find . -name '*.pyc ' -delete

prepare:clean
	set -ex
	python3 -m venv venv
	#venv/bin/pip3 install -r requirements.txt
	venv/bin/pip3 install llama-index-core llama_index
	venv/bin/pip3 install llama-index-embeddings-llamafile llama-index-llms-llamafile llama-index-readers-web
	#venv/bin/pip3 install llama_index
	

start_llm:
	../llava-v1.5-7b-q4.llamafile -ngl 9999 --server --nobrowser --embedding --port 8080

prepare_data:
	venv/bin/python prepare_data.py
