//package kz.aihackathon.aiprocure.service.parser;
//
//import io.github.bonigarcia.wdm.WebDriverManager;
//import kz.aihackathon.aiprocure.model.Tender;
//import kz.aihackathon.aiprocure.repository.tender.TenderRepository;
//import org.openqa.selenium.By;
//import org.openqa.selenium.WebDriver;
//import org.openqa.selenium.WebElement;
//import org.openqa.selenium.chrome.ChromeDriver;
//import org.openqa.selenium.chrome.ChromeOptions;
//import org.springframework.stereotype.Service;
//
//import java.time.LocalDateTime;
//import java.util.HashMap;
//import java.util.List;
//import java.util.Map;
//
//@Service
//public class TenderParserService {
//
//    private final TenderRepository tenderRepository;
//
//    public TenderParserService(TenderRepository tenderRepository) {
//        this.tenderRepository = tenderRepository;
//    }
//
//    public void parseAndSaveTenders() {
//        WebDriverManager.chromedriver().setup();
//        ChromeOptions options = new ChromeOptions();
//        options.addArguments("--headless"); // без GUI
//        options.addArguments("--no-sandbox");
//        options.addArguments("--disable-dev-shm-usage");
//
//        WebDriver driver = new ChromeDriver(options);
//
//        try {
//            driver.get("https://goszakup.gov.kz/ru/search/announce");
//
//            // Ждём, пока страница загрузится
//            Thread.sleep(5000);
//
//            List<WebElement> tenderElements = driver.findElements(By.cssSelector(".tender-item")); // пример селектора
//
//            for (WebElement element : tenderElements) {
//                String rawText = element.getText();
//
//                // Простейший пример извлечения данных
//                Map<String, Object> extractedFields = new HashMap<>();
//                try {
//                    extractedFields.put("title", element.findElement(By.cssSelector(".tender-title")).getText());
//                    extractedFields.put("price", element.findElement(By.cssSelector(".tender-price")).getText());
//                    extractedFields.put("deadline", element.findElement(By.cssSelector(".tender-deadline")).getText());
//                } catch (Exception ignored) {}
//
//                // Заглушки для supplierMatches и riskAnalysis
//                Map<String, Object> supplierMatches = new HashMap<>();
//                Map<String, Object> riskAnalysis = new HashMap<>();
//
//                Tender tender = new Tender();
//                tender.setRawText(rawText);
//                tender.setExtractedFields(extractedFields);
//                tender.setSupplierMatches(supplierMatches);
//                tender.setRiskAnalysis(riskAnalysis);
//                tender.setFallback(false);
//                tender.setCreatedAt(LocalDateTime.now());
//
//                tenderRepository.save(tender);
//            }
//
//        } catch (Exception e) {
//            e.printStackTrace();
//        } finally {
//            driver.quit();
//        }
//    }
//}
