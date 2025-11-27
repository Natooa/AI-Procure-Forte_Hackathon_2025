package kz.aihackathon.aiprocure.service.parser;

import kz.aihackathon.aiprocure.model.Tender;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class TextParser {

    public Tender parseUrlToTender(String url) {
        Tender tender = new Tender();
        Map<String, Object> extractedFields = new HashMap<>();

        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless", "--no-sandbox", "--disable-dev-shm-usage");

        WebDriver driver = new ChromeDriver(options);

        try {
            driver.get(url);
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));

            // --- Title ---
            WebElement titleInput = wait.until(
                    ExpectedConditions.visibilityOfElementLocated(
                            By.xpath("//label[text()='Наименование объявления']/following-sibling::div/input")
                    )
            );
            String title = titleInput.getAttribute("value");

            // --- Start Date ---
            WebElement startInput = wait.until(
                    ExpectedConditions.visibilityOfElementLocated(
                            By.xpath("//label[text()='Срок начала приема заявок']/following-sibling::div/input")
                    )
            );
            String startDate = startInput.getAttribute("value");

            // --- End Date ---
            WebElement endInput = wait.until(
                    ExpectedConditions.visibilityOfElementLocated(
                            By.xpath("//label[text()='Срок окончания приема заявок']/following-sibling::div/input")
                    )
            );
            String endDate = endInput.getAttribute("value");

            // --- Remaining Time ---
            WebElement remainingDiv = wait.until(
                    ExpectedConditions.visibilityOfElementLocated(
                            By.xpath("//label[text()='Оставшееся время']/following-sibling::div//div[@id='asNeeded']")
                    )
            );
            String remainingTime = remainingDiv.getText();

            tender.setRawText("Название: " + title + "\nДата начала: " + startDate + "\nДата окончания: " + endDate);

            extractedFields.put("title", title);
            extractedFields.put("startDate", startDate);
            extractedFields.put("endDate", endDate);
            extractedFields.put("remainingTime", remainingTime);

            // --- Общие сведения ---
            WebElement generalInfoPanel = driver.findElement(
                    By.xpath("//div[@class='panel-heading']/b[text()='Общие сведения']/ancestor::div[@class='panel panel-default']")
            );
            List<WebElement> rows = generalInfoPanel.findElements(By.xpath(".//tr"));
            Map<String, String> generalInfo = new HashMap<>();
            for (WebElement row : rows) {
                try {
                    String key = row.findElement(By.tagName("th")).getText().trim();
                    String value = row.findElement(By.tagName("td")).getText().trim();
                    generalInfo.put(key, value);
                } catch (Exception ignored) {}
            }
            extractedFields.put("generalInfo", generalInfo);

            // --- Остальные таблицы ---
            List<WebElement> tables = driver.findElements(By.cssSelector("div.panel-default > table"));
            Map<String, String> tableData = new HashMap<>();
            for (WebElement table : tables) {
                for (WebElement row : table.findElements(By.tagName("tr"))) {
                    try {
                        String key = row.findElement(By.tagName("th")).getText().trim();
                        String value = row.findElement(By.tagName("td")).getText().trim();
                        tableData.put(key, value);
                    } catch (Exception ignored) {}
                }
            }
            extractedFields.put("tableData", tableData);

            tender.setExtractedFields(extractedFields);

        } catch (Exception e) {
            e.printStackTrace();
            tender.setFallback(true);
        } finally {
            driver.quit();
        }

        return tender;
    }
}
