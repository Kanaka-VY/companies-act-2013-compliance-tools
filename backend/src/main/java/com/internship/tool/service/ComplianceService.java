package com.internship.tool.service;

import java.time.Instant;
import java.util.Map;

import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.internship.tool.entity.Compliance;
import com.internship.tool.repository.ComplianceRepository;

@Service
public class ComplianceService {

    private final ComplianceRepository complianceRepository;
    private final AiServiceClient aiServiceClient;
    private final ObjectMapper objectMapper;

    public ComplianceService(
            ComplianceRepository complianceRepository,
            AiServiceClient aiServiceClient,
            ObjectMapper objectMapper) {
        this.complianceRepository = complianceRepository;
        this.aiServiceClient = aiServiceClient;
        this.objectMapper = objectMapper;
    }

    public Compliance create(String recordText) {
        Compliance compliance = new Compliance();
        compliance.setRecordText(recordText);
        Compliance saved = complianceRepository.save(compliance);
        enrichWithAiAsync(saved.getId(), recordText);
        return saved;
    }

    @Async
    public void enrichWithAiAsync(Long complianceId, String recordText) {
        Compliance compliance = complianceRepository.findById(complianceId).orElse(null);
        if (compliance == null) {
            return;
        }

        Map<String, Object> describe = aiServiceClient.describe(recordText);
        Map<String, Object> recommend = aiServiceClient.recommend(recordText);
        Map<String, Object> report = aiServiceClient.generateReport(recordText);

        if (describe != null) {
            compliance.setAiDescription(stringOrNull(describe.get("description")));
            compliance.setAiRiskLevel(stringOrNull(describe.get("risk_level")));
        }
        if (recommend != null) {
            compliance.setAiRecommendationsJson(asJsonOrNull(recommend.get("recommendations")));
        }
        if (report != null) {
            compliance.setAiReportJson(asJsonOrNull(report));
        }
        if (describe != null || recommend != null || report != null) {
            compliance.setAiGeneratedAt(Instant.now());
            complianceRepository.save(compliance);
        }
    }

    private String stringOrNull(Object value) {
        return value == null ? null : String.valueOf(value);
    }

    private String asJsonOrNull(Object value) {
        if (value == null) {
            return null;
        }
        try {
            return objectMapper.writeValueAsString(value);
        } catch (JsonProcessingException ex) {
            return null;
        }
    }
}
