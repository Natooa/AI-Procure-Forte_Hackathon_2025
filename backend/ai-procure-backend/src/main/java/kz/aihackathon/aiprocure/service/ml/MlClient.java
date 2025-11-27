package kz.aihackathon.aiprocure.service.ml;

import kz.aihackathon.aiprocure.dto.extract.ExtractRequest;
import kz.aihackathon.aiprocure.dto.extract.ExtractResponse;
import kz.aihackathon.aiprocure.dto.match.MatchRequest;
import kz.aihackathon.aiprocure.dto.match.MatchResponse;
import kz.aihackathon.aiprocure.dto.risk.RiskRequest;
import kz.aihackathon.aiprocure.dto.risk.RiskResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
@RequiredArgsConstructor
public class MlClient {

    private final WebClient webClient;

    @Value("${ml.url}")
    private String mlUrl;

    public ExtractResponse extract(ExtractRequest request) {
        return webClient.post()
                .uri(mlUrl + "/extract")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ExtractResponse.class)
                .block();
    }

    public MatchResponse match(MatchRequest request){
        return webClient.post()
                .uri(mlUrl + "/match")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(MatchResponse.class)
                .block();
    }

    public RiskResponse risk(RiskRequest request){
        return webClient.post()
                .uri(mlUrl + "/risk")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(RiskResponse.class)
                .block();
    }

}
