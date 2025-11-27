package kz.aihackathon.aiprocure.service.parser;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class TextParser {

    public String parseUrl(String url) {
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless"); // Без окна браузера
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-dev-shm-usage");

        WebDriver driver = new ChromeDriver(options);
        StringBuilder resultText = new StringBuilder();

        try {
            driver.get(url);
            Thread.sleep(5000); // Ждем загрузку страницы, можно заменить на WebDriverWait

            // 1. Основные input'ы (название, даты)
            String title = driver.findElement(By.cssSelector("input[readonly][value*='Приобретение']")).getAttribute("value");
            String startDate = driver.findElement(By.xpath("//label[text()='Срок начала приема заявок']/following-sibling::div/input")).getAttribute("value");
            String endDate = driver.findElement(By.xpath("//label[text()='Срок окончания приема заявок']/following-sibling::div/input")).getAttribute("value");
            String remainingTime = driver.findElement(By.id("asNeeded")).getText();

            resultText.append("Название закупки: ").append(title).append("\n");
            resultText.append("Начало приема заявок: ").append(startDate).append("\n");
            resultText.append("Окончание приема заявок: ").append(endDate).append("\n");
            resultText.append("Оставшееся время: ").append(remainingTime).append("\n\n");

            // 2. Данные из таблиц
            List<WebElement> tables = driver.findElements(By.cssSelector("div.panel-default > table"));
            Map<String, String> dataMap = new HashMap<>();

            for (WebElement table : tables) {
                List<WebElement> rows = table.findElements(By.tagName("tr"));
                for (WebElement row : rows) {
                    try {
                        String key = row.findElement(By.tagName("th")).getText().trim();
                        String value = row.findElement(By.tagName("td")).getText().trim();
                        dataMap.put(key, value);
                    } catch (Exception e) {
                        // Пропускаем строки без th/td
                    }
                }
            }

            // Добавляем данные таблиц к результату
            dataMap.forEach((k, v) -> resultText.append(k).append(": ").append(v).append("\n"));

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            driver.quit();
        }

        return resultText.toString();
    }

    public String parseFile(MultipartFile file) {
        return "dont work";
    }
}
