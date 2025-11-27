package kz.aihackathon.aiprocure.model;

import jakarta.persistence.*;
import kz.aihackathon.aiprocure.config.MapToJsonConverter;
import lombok.*;

import java.time.LocalDateTime;
import java.util.Map;

@Entity
@Data
public class Tender {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String rawText;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = MapToJsonConverter.class)
    private Map<String, Object> extractedFields;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = MapToJsonConverter.class)
    private Map<String, Object> supplierMatches;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = MapToJsonConverter.class)
    private Map<String, Object> riskAnalysis;

    private Boolean fallback = false;

    private LocalDateTime createdAt = LocalDateTime.now();
}
