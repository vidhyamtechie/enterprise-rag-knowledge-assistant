package com.venkatesh.ai.rag.model;

import java.util.List;

public record ChatResponse(
        String answer,
        List<Source> sources
) {}
