package kz.aihackathon.aiprocure.model;

import jakarta.persistence.*;
import kz.aihackathon.aiprocure.config.MapToJsonConverter;
import lombok.*;

import java.time.LocalDateTime;
import java.util.Map;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Tender {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String rawText;

    @Convert(converter = MapToJsonConverter.class)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> extractedFields;

    @Convert(converter = MapToJsonConverter.class)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> supplierMatches;

    @Convert(converter = MapToJsonConverter.class)
    @Column(columnDefinition = "jsonb")
    private Map<String, Object> riskAnalysis;

    private Boolean fallback = false;

    private LocalDateTime createdAt;

    @PrePersist
    public void prePersist() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }
}
