package com.ai.gateway.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@RequestMapping("/ai")
public class AiController {

    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/ask")
    public String askQuestion(@RequestBody Map<String, String> request) {
        String question = request.get("question");

        String url = "http://localhost:8001/generate";

        Map<String, String> body = Map.of("question", question);

        String response = restTemplate.postForObject(url, body, String.class);

        return response;
    }
}