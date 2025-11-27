package kz.aihackathon.aiprocure.dto;

import kz.aihackathon.aiprocure.model.Tender;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.Map;

@Data
public class TenderDto {
    private Long id;
    private String rawText;
    private Map<String, Object> extractedFields;
    private Map<String, Object> supplierMatches;
    private Map<String, Object> riskAnalysis;
    private Boolean fallback;
    private LocalDateTime createdAt;

    public static TenderDto fromEntity(Tender tender) {
        TenderDto dto = new TenderDto();
        dto.setId(tender.getId());
        dto.setRawText(tender.getRawText());
        dto.setExtractedFields(tender.getExtractedFields());
        dto.setSupplierMatches(tender.getSupplierMatches());
        dto.setRiskAnalysis(tender.getRiskAnalysis());
        dto.setFallback(tender.getFallback());
        dto.setCreatedAt(tender.getCreatedAt());
        return dto;
    }
}
