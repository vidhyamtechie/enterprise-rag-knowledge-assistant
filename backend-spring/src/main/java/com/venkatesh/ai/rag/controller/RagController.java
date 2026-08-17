package com.venkatesh.ai.rag.controller;

import com.venkatesh.ai.rag.model.ChatRequest;
import com.venkatesh.ai.rag.model.ChatResponse;
import com.venkatesh.ai.rag.service.RagClient;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/rag")
@CrossOrigin(origins = "http://localhost:4200")
public class RagController {
    private final RagClient ragClient;

    public RagController(RagClient ragClient) {
        this.ragClient = ragClient;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<?, ?>> health() {
        return ResponseEntity.ok(ragClient.health());
    }

    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(
            @Valid @RequestBody ChatRequest request
    ) {
        return ResponseEntity.ok(ragClient.chat(request));
    }

    @PostMapping("/ingest-directory")
    public ResponseEntity<Map<?, ?>> ingestDirectory() {
        return ResponseEntity.ok(ragClient.ingestDirectory());
    }
}
