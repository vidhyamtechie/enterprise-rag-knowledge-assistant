package com.venkatesh.ai.rag.model;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public record ChatRequest(
        @NotBlank String question,
        @Min(1) @Max(20) Integer topK
) {}
