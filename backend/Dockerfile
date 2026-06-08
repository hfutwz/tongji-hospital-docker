# ============================================
# 后端 Dockerfile
# ============================================
FROM maven:3.8-openjdk-8 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests -B

# 运行阶段：使用 Azul Zulu OpenJDK 8 Alpine
FROM azul/zulu-openjdk-alpine:8
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
# 等待 MySQL/Redis 就绪的工具
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.1/wait /wait
RUN chmod +x /wait
EXPOSE 9090
CMD /wait && java -jar app.jar --spring.profiles.active=prod