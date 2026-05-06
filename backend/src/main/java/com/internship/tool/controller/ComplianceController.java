package com.internship.tool.controller;

import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.internship.tool.entity.Compliance;
import com.internship.tool.service.ComplianceService;

@RestController
@RequestMapping("/api/compliance")
public class ComplianceController {

    private final ComplianceService complianceService;

    public ComplianceController(ComplianceService complianceService) {
        this.complianceService = complianceService;
    }

    @PostMapping
    public ResponseEntity<Compliance> create(@RequestBody Map<String, String> body) {
        String recordText = body.getOrDefault("recordText", "").trim();
        if (recordText.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok(complianceService.create(recordText));
    }
}
