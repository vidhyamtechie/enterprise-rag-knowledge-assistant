package com.venkatesh.ai.rag.service;

import com.venkatesh.ai.rag.model.ChatRequest;
import com.venkatesh.ai.rag.model.ChatResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class RagClient {
    private final RestClient restClient;

    public RagClient(
            RestClient.Builder builder,
            @Value("${rag.service.base-url}") String baseUrl
    ) {
        this.restClient = builder.baseUrl(baseUrl).build();
    }

    public ChatResponse chat(ChatRequest request) {
        return restClient.post()
                .uri("/api/chat")
                .body(Map.of(
                        "question", request.question(),
                        "top_k", request.topK() == null ? 5 : request.topK()
                ))
                .retrieve()
                .body(ChatResponse.class);
    }

    public Map<?, ?> health() {
        return restClient.get()
                .uri("/api/health")
                .retrieve()
                .body(Map.class);
    }

    public Map<?, ?> ingestDirectory() {
        return restClient.post()
                .uri("/api/ingest/directory")
                .retrieve()
                .body(Map.class);
    }
}
