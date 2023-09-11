# llama_cpp_server

This is an experimental repo that uses llama.cpp for LLM applications.

- `compose.yml` contains the setup for the llama.cpp docker containers, which includes `convert`, `quantize` and `server` services
  - `docker-compose run convert`
  - `docker-compose run quantize`
  - `docker-compose up server_host`
- `index.js` is used to run `server` service test.

## Reference

- [llama.cpp](https://github.com/ggerganov/llama.cpp)

  - To run services through Docker container, given `MODELS_PATH = /home/sen/dev/codellama/`, `TARGET_MODEL=CodeLlama-7b`
    - `docker run -v /home/sen/dev/codellama/:/models ghcr.io/ggerganov/llama.cpp:full --convert "/models/CodeLlama-7b/"`
    - `docker run -v /home/sen/dev/codellama/:/models ghcr.io/ggerganov/llama.cpp:full --quantize "/models/CodeLlama-7b/ggml-model-f16.gguf" "/models/CodeLlama-7b/ggml-model-q4_0.gguf" 2`
    - `docker run -v /home/sen/dev/codellama/:/models ghcr.io/ggerganov/llama.cpp:full --run -m /models/CodeLlama-7b/ggml-model-f16.gguf -p "Building a website can be done in 5 simple steps:" -n 512`
  - [llama.cpp HTTP API server](https://github.com/ggerganov/llama.cpp/tree/master/examples/server)
    - `docker run -v /home/sen/dev/codellama/:/models --network host ghcr.io/ggerganov/llama.cpp:full --server -m /models/CodeLlama-7b/ggml-model-q4_0.gguf -c 2048 --port 8080`
    - [--server with docker port binding issue](https://github.com/ggerganov/llama.cpp/issues/2992)

- [Signal LLM Compress](https://github.com/Wheest/signal-compress/tree/main), an example application that uses llama.cpp.
  - [Detailed setup](https://github.com/Wheest/wheest.github.io/blob/6a5e0c1ff075a03d3ed2c778243e878d767b39ba/_posts/2023-09-05-signal_compress_docker_compose.md)
- [llama2-webui](https://github.com/liltom-eth/llama2-webui)
