package com.internship.tool.entity;

import java.time.Instant;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;

@Entity
public class Compliance {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 2000)
    private String recordText;

    private String aiRiskLevel;

    @Lob
    private String aiDescription;

    @Lob
    private String aiRecommendationsJson;

    @Lob
    private String aiReportJson;

    private Instant aiGeneratedAt;

    public Long getId() {
        return id;
    }

    public String getRecordText() {
        return recordText;
    }

    public void setRecordText(String recordText) {
        this.recordText = recordText;
    }

    public String getAiRiskLevel() {
        return aiRiskLevel;
    }

    public void setAiRiskLevel(String aiRiskLevel) {
        this.aiRiskLevel = aiRiskLevel;
    }

    public String getAiDescription() {
        return aiDescription;
    }

    public void setAiDescription(String aiDescription) {
        this.aiDescription = aiDescription;
    }

    public String getAiRecommendationsJson() {
        return aiRecommendationsJson;
    }

    public void setAiRecommendationsJson(String aiRecommendationsJson) {
        this.aiRecommendationsJson = aiRecommendationsJson;
    }

    public String getAiReportJson() {
        return aiReportJson;
    }

    public void setAiReportJson(String aiReportJson) {
        this.aiReportJson = aiReportJson;
    }

    public Instant getAiGeneratedAt() {
        return aiGeneratedAt;
    }

    public void setAiGeneratedAt(Instant aiGeneratedAt) {
        this.aiGeneratedAt = aiGeneratedAt;
    }
}
