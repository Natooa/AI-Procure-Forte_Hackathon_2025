package kz.aihackathon.aiprocure.dto.match;

import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
public class MatchResponse {
    private String tenderId;
    private List<Map<String, Object>> matches;
}
