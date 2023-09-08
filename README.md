# llama_cpp_server

This is an experimental repo which leveages llama.cpp for LLM applications

- compose.yml contains the configuration of llama.cpp docker containers, which has `convert`, `quantize` and `server` services
- index.js is used to test `server` service.

## Reference

- [llama.cpp](https://github.com/ggerganov/llama.cpp)
  - [llama.cpp HTTP API server](https://github.com/ggerganov/llama.cpp/tree/master/examples/server)
- [Signal LLM Compress](https://github.com/Wheest/signal-compress/tree/main), application example which adopts llama.cpp.
  - [Detailed setup](https://github.com/Wheest/wheest.github.io/blob/6a5e0c1ff075a03d3ed2c778243e878d767b39ba/_posts/2023-09-05-signal_compress_docker_compose.md)
- [llama2-webui](https://github.com/liltom-eth/llama2-webui)
