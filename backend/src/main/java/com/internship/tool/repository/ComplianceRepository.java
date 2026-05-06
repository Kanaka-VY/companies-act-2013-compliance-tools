package com.internship.tool.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.internship.tool.entity.Compliance;

public interface ComplianceRepository extends JpaRepository<Compliance, Long> {
}
