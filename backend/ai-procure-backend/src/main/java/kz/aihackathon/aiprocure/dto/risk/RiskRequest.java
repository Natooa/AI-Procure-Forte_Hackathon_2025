package kz.aihackathon.aiprocure.dto.risk;

import lombok.Data;

import java.util.Map;

@Data
public class RiskRequest {
    private String tenderId;
    private Map<String, Object> features;
}
