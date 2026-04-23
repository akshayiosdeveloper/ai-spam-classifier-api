//
//  SpamDectorDashBoard.swift
//  AI SpamGuard
//
//  Created by Akshay Kumar on 22/04/26.
//

import SwiftUI

struct SpamDectorDashBoard: View {
    
    @State private var message: String = ""
    @State private var prediction: String = ""
    @State private var confidence: Double = 0.0
    @State private var level: String = ""
    @State private var isLoading: Bool = false
    @State private var messages: [ChatMessage] = []
    
    var body: some View {
        VStack {
            
            
            Text("AI SpamGuard ")
                .font(.title)
                .bold()
                .padding(.top, 20)
            
            
            if messages.isEmpty {
                Spacer()
                
                VStack(spacing: 10) {
                    Text("Start checking messages")
                        .font(.headline)
                    
                    Text("Type a message below to detect spam")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                }
                
                Spacer()
            } else {
                ScrollViewReader { proxy in
                    ScrollView {
                        VStack(spacing: 10) {
                            ForEach(messages) { msg in
                                HStack {
                                    
                                    if msg.isUser {
                                        Spacer()
                                        
                                        Text(msg.text)
                                            .padding()
                                            .background(Color.blue)
                                            .foregroundColor(.white)
                                            .cornerRadius(12)
                                    } else {
                                        if msg.isTyping {
                                            TypingIndicatorView()
                                                .padding()
                                                .background(Color.gray.opacity(0.2))
                                                .cornerRadius(10)
                                        }else {
                                            VStack(alignment: .leading, spacing: 5) {
                                                
                                                Text(msg.prediction?.uppercased() ?? "")
                                                    .bold()
                                                    .foregroundColor(msg.prediction == "spam" ? .red : .green)
                                                
                                                Text("Confidence: \(String(format: "%.2f", msg.confidence ?? 0))")
                                                
                                                Text("Level: \(msg.level ?? "")")
                                            }
                                            .padding()
                                            .background(Color(.systemGray6))
                                            .cornerRadius(12)
                                        }
                                        Spacer()
                                    }
                                }
                                .padding(.horizontal)
                                .id(msg.id)
                            }
                        }
                    }
                    .onChange(of: messages.count) { _, _ in
                        if let last = messages.last {
                            withAnimation {
                                proxy.scrollTo(last.id, anchor: .bottom)
                            }
                        }
                    }
                }
                
            }
            
            
            HStack(spacing:10) {
                TextField("Type a message...", text: $message)
                    .padding(12)
                    .background(Color(.systemGray6))
                    .cornerRadius(20)
                
                Button(action: {
                    sendMessage()
                }) {
                    Image(systemName: "paperplane.fill")
                        .foregroundColor(.white)
                        .padding(10)
                        .background(message.trimmingCharacters(in: .whitespaces).isEmpty ? Color.gray : Color.blue)
                        .clipShape(Circle())
                }
                .disabled(message.trimmingCharacters(in: .whitespaces).isEmpty)
            }
            .padding()
            .background(Color.white)
        }
    }
    
    func predictSpam(message: String) {
        
        guard let url = URL(string: "http://127.0.0.1:8000/predict") else { return }
        
        let requestBody = PredictRequest(message: message)
        
        guard let jsonData = try? JSONEncoder().encode(requestBody) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, _, _ in
            
            guard let data = data,
                  let decoded = try? JSONDecoder().decode(PredictResponse.self, from: data) else {
                return
            }
            
            DispatchQueue.main.async {
                
                // ✅ 1. Remove typing indicator FIRST
                if let index = self.messages.lastIndex(where: { message in
                    message.isTyping == true
                }) {
                    self.messages.remove(at: index)
                }
                
               // let formattedResponse = self.formatResponse(decoded)
               
               // DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                    //self.streamResponse(formattedResponse, prediction: decoded.prediction, confidence: decoded.confidence, level: decoded.level)
                let aiMessage = ChatMessage(
                    text: "",
                    isUser: false,
                    prediction: decoded.prediction,
                    confidence: decoded.confidence,
                    level: decoded.level,
                    isTyping: false,
                    isStreaming: true
                )
                messages.append(aiMessage)
               // }
            }
            
        }.resume()
    }
    
    func formatResponse(_ response: PredictResponse) -> String {
        return """
        AI Status : \(response.prediction)
        Confidence: \(String(format: "%.2f", response.confidence))
        Level: \(response.level)
        """
    }
    func sendMessage() {
        let userText = message   // ✅ store first
        
        let userMessage = ChatMessage(
            text: userText,
            isUser: true,
            prediction: nil,
            confidence: nil,
            level: nil,
            isTyping: false, isStreaming: false
        )
        
        messages.append(userMessage)
        message = ""
        
        // typing indicator
        let typingMessage = ChatMessage(
            text: "",
            isUser: false,
            prediction: nil,
            confidence: nil,
            level: nil,
            isTyping: true, isStreaming: false
        )
        
        messages.append(typingMessage)
        
        // ✅ pass correct message
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
            predictSpam(message: userText)
        }
    }
    
    func streamResponse(_ fullText: String,prediction: String,confidence: Double,level: String) {
        
        let words = fullText.split(separator: " ")
    
        let aiMessage = ChatMessage(
            text: "",
            isUser: false,
            prediction: prediction,
            confidence: confidence,
            level: level,
            isTyping: false,
            isStreaming: true
        )
        messages.append(aiMessage)
        
        guard let index = messages.indices.last else { return }

        for (i, word) in words.enumerated() {
            
            DispatchQueue.main.asyncAfter(deadline: .now() + Double(i) * 0.8) {
                
                self.messages[index].text += word + " "
                
                if i == words.count - 1 {
                    self.messages[index].isStreaming = false
                }
            }
        }
    }
}

#Preview {
    SpamDectorDashBoard()
}

