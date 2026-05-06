package com.internship.tool.service;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class AiServiceClient {

    private final RestTemplate restTemplate;
    private final String aiServiceBaseUrl;

    public AiServiceClient(
            RestTemplate restTemplate,
            @Value("${ai.service.base-url:http://localhost:8000}") String aiServiceBaseUrl) {
        this.restTemplate = restTemplate;
        this.aiServiceBaseUrl = aiServiceBaseUrl;
    }

    public Map<String, Object> describe(String record) {
        return post("/describe", record);
    }

    public Map<String, Object> recommend(String record) {
        return post("/recommend", record);
    }

    public Map<String, Object> generateReport(String record) {
        return post("/generate-report", record);
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> post(String path, String record) {
        try {
            Map<String, String> body = new HashMap<>();
            body.put("record", record);
            ResponseEntity<Map> response =
                    restTemplate.postForEntity(aiServiceBaseUrl + path, body, Map.class);
            return response.getBody();
        } catch (Exception ex) {
            return null;
        }
    }
}
