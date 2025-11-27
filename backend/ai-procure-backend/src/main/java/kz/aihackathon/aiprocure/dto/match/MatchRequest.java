package kz.aihackathon.aiprocure.dto.match;

import lombok.Data;

@Data
public class MatchRequest {
    private String tenderId;
    private String title;
    private String subject;
    private Integer topK;
}
