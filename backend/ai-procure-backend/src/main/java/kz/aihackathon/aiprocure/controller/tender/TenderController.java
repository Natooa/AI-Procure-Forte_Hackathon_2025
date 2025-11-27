package kz.aihackathon.aiprocure.controller.tender;

import kz.aihackathon.aiprocure.dto.TenderDto;
import kz.aihackathon.aiprocure.service.tender.TenderService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/tenders")
@RequiredArgsConstructor
public class TenderController {

    private final TenderService tenderService;

    @PostMapping("/ingest/url")
    public TenderDto ingestUrl(@RequestParam String url) {
        return TenderDto.fromEntity(tenderService.ingestFromUrl(url));
    }

    @PostMapping("/ingest/upload")
    public TenderDto ingestFile(@RequestParam MultipartFile file) {
        return TenderDto.fromEntity(tenderService.ingestFromFile(file));
    }

    @GetMapping("/{id}")
    public TenderDto get(@PathVariable Long id) {
        return TenderDto.fromEntity(tenderService.getById(id));
    }
}

