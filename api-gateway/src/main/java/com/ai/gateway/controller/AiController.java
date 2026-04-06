package com.ai.gateway.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@RequestMapping("/ai")
public class AiController {

    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/test")
    public String test() {
        return "API Gateway working!";
    }

    @PostMapping("/ask")
    public String askQuestion(@RequestBody Map<String, String> request) {
        String question = request.get("question");
        String url = "http://localhost:8001/generate";
        Map<String, String> body = Map.of("prompt", question);

        Map response = restTemplate.postForObject(url, body, Map.class);
        return response.get("response").toString();
    }
}