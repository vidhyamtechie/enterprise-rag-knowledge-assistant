package com.venkatesh.ai.rag.model;

public record Source(
        String source,
        Integer page,
        String chunk_id,
        Double distance
) {}
