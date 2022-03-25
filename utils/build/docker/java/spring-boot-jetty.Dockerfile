FROM maven:3.3-jdk-8 as build

WORKDIR /app

COPY ./utils/build/docker/java/install_ddtrace.sh binaries* /binaries/
RUN /binaries/install_ddtrace.sh

COPY ./utils/build/docker/java/spring-boot/pom.xml .
RUN mkdir /maven && mvn -Dmaven.repo.local=/maven -Pjetty -B dependency:go-offline

COPY ./utils/build/docker/java/spring-boot/src ./src
RUN mvn -Dmaven.repo.local=/maven -Pjetty package

FROM adoptopenjdk:11-jre-hotspot

WORKDIR /app
COPY --from=build /binaries/SYSTEM_TESTS_LIBRARY_VERSION SYSTEM_TESTS_LIBRARY_VERSION
COPY --from=build /binaries/SYSTEM_TESTS_LIBDDWAF_VERSION SYSTEM_TESTS_LIBDDWAF_VERSION
COPY --from=build /binaries/SYSTEM_TESTS_APPSEC_EVENT_RULES_VERSION SYSTEM_TESTS_APPSEC_EVENT_RULES_VERSION
COPY --from=build /app/target/myproject-0.0.1-SNAPSHOT.jar .
COPY --from=build /dd-tracer/dd-java-agent.jar .

RUN echo "#!/bin/bash\njava -javaagent:/app/dd-java-agent.jar -jar /app/myproject-0.0.1-SNAPSHOT.jar --server.port=7777" > app.sh
RUN chmod +x app.sh
CMD [ "./app.sh" ]