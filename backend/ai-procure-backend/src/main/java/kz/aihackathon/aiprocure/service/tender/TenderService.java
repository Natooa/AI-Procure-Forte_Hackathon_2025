package kz.aihackathon.aiprocure.service.tender;

import kz.aihackathon.aiprocure.dto.extract.ExtractRequest;
import kz.aihackathon.aiprocure.dto.extract.ExtractResponse;
import kz.aihackathon.aiprocure.dto.match.MatchRequest;
import kz.aihackathon.aiprocure.dto.match.MatchResponse;
import kz.aihackathon.aiprocure.dto.risk.RiskRequest;
import kz.aihackathon.aiprocure.dto.risk.RiskResponse;
import kz.aihackathon.aiprocure.model.Tender;
import kz.aihackathon.aiprocure.repository.tender.TenderRepository;
import kz.aihackathon.aiprocure.service.ml.MlClient;
import kz.aihackathon.aiprocure.service.parser.TextParser;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class TenderService {

    private final TextParser textParser;
    private final MlClient mlClient;
    private final TenderRepository tenderRepository;

    public Tender ingestFromText(String rawText) {
        String tenderId = "T" + System.currentTimeMillis();
        Tender tender = new Tender();
        tender.setRawText(rawText);

        try {
            processMlPipeline(tender, tenderId, rawText);
            tender.setFallback(false);
        } catch (Exception e) {
            tender.setFallback(true);
            tender.setExtractedFields(null);
            tender.setSupplierMatches(null);
            tender.setRiskAnalysis(null);
        }

        return tenderRepository.save(tender);
    }

    private void processMlPipeline(Tender tender, String tenderId, String rawText) {
        // --- Extract ---
        ExtractRequest extractReq = new ExtractRequest();
        extractReq.setTenderId(tenderId);
        extractReq.setText(rawText);
        ExtractResponse extracted = mlClient.extract(extractReq);
        tender.setExtractedFields(extracted.getExtracted());

        // --- Match ---
        MatchRequest matchReq = new MatchRequest();
        matchReq.setTenderId(extracted.getTenderId());
        matchReq.setTitle((String) extracted.getExtracted().getOrDefault("title", ""));
        matchReq.setSubject("default");
        matchReq.setTopK(5);
        MatchResponse matches = mlClient.match(matchReq);
        tender.setSupplierMatches(Map.of("matches", matches.getMatches()));

        // --- Risk ---
        RiskRequest riskReq = new RiskRequest();
        riskReq.setTenderId(extracted.getTenderId());
        Map<String, Object> features = new HashMap<>();
        features.put("extracted", extracted.getExtracted());
        features.put("matches", matches.getMatches());
        riskReq.setFeatures(features);
        RiskResponse risk = mlClient.risk(riskReq);
        tender.setRiskAnalysis(Map.of(
                "score", risk.getRiskScore(),
                "reasons", risk.getRiskReasons()
        ));
    }

    public Tender ingestFromUrl(String url) {
        String text = textParser.parseUrl(url);
        return ingestFromText(text);
    }

    public Tender ingestFromFile(MultipartFile file) {
        String text = textParser.parseFile(file);
        return ingestFromText(text);
    }

    public Tender getById(Long id) {
        return tenderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Tender not found with id: " + id));
    }
}
