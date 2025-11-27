package kz.aihackathon.aiprocure.dto.risk;

import lombok.Data;

import java.util.List;

@Data
public class RiskResponse {
    private String tenderId;
    private Double riskScore;
    private List<String> riskReasons;
}
