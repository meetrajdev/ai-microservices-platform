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
    public Map<String, String> askQuestion(@RequestBody Map<String, String> request) {
        String question = request.get("question");

        // STEP 1: Call vector service
        String vectorUrl = "http://localhost:8001/search";
        Map<String, String> searchBody = Map.of("query", question);
        Map vectorResponse = restTemplate.postForObject(vectorUrl, searchBody, Map.class);
        String context = (String) vectorResponse.get("context");

        // STEP 2: Build prompt
        String finalPrompt = "Answer based on context: " + context + "\nQuestion: " + question;

        // STEP 3: Call model service
        String modelUrl = "http://localhost:8002/generate";
        Map<String, String> modelBody = Map.of("prompt", finalPrompt);
        Map modelResponse = restTemplate.postForObject(modelUrl, modelBody, Map.class);

        return modelResponse;
    }
}