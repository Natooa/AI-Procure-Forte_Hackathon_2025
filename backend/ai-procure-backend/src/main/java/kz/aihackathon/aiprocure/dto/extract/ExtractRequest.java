package kz.aihackathon.aiprocure.dto.extract;

import lombok.Data;

@Data
public class ExtractRequest {
    private String tenderId;
    private String text;
}
