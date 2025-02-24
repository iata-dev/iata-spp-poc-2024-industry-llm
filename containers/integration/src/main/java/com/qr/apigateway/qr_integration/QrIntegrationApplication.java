package com.qr.apigateway.qr_integration;

import com.qr.apigateway.qr_integration.snowflake.SnowFlakeInteg;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import java.security.Security;
import org.bouncycastle.jcajce.provider.BouncyCastleFipsProvider;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.context.annotation.ComponentScan;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLSession;

@SpringBootApplication
@ComponentScan
public class QrIntegrationApplication extends SpringBootServletInitializer {

	public static void main(String[] args) {
		SpringApplication.run(QrIntegrationApplication.class, args);
        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
         //   Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }

        Security.addProvider(new BouncyCastleFipsProvider());
	HttpsURLConnection.setDefaultHostnameVerifier(new HostnameVerifier() {
			@Override
			public boolean verify(String hostname, SSLSession session) {
				// Implement custom verification logic
				return "ec2-3-83-84-66.compute-1.amazonaws.com".equalsIgnoreCase(hostname);
			}
		});

	}

}
