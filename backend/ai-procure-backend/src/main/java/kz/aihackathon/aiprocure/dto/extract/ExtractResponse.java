package kz.aihackathon.aiprocure.dto.extract;

import lombok.Data;

import java.util.Map;

@Data
public class ExtractResponse {
    private String tenderId;
    private Map<String, Object> extracted;
}
