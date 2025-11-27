# --- Сборка через Maven ---
FROM maven:3.9.2-eclipse-temurin-17 AS build

WORKDIR /app

# Сначала копируем только pom.xml, чтобы закешировать зависимости
COPY pom.xml .
RUN mvn dependency:go-offline

# Потом копируем исходники и собираем проект
COPY src ./src
RUN mvn clean package -DskipTests

# --- Финальный образ на Ubuntu 22.04 ---
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# --- Устанавливаем системные зависимости ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    wget \
    unzip \
    curl \
    gnupg2 \
    libnss3 \
    libxi6 \
    libxrender1 \
    libxrandr2 \
    libatk1.0-0 \
    libgtk-3-0 \
    fonts-liberation \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# --- Устанавливаем Google Chrome (отдельный слой для кэширования) ---
ARG CHROME_DEB_URL=https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN wget -q -O /tmp/chrome.deb $CHROME_DEB_URL \
    && apt-get update && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

# Копируем собранный jar
COPY --from=build /app/target/ai-procure-backend-*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
