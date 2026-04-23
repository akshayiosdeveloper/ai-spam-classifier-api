//
//  ChatMessage.swift
//  AI SpamGuard
//
//  Created by Akshay Kumar on 22/04/26.
//

import Foundation

struct ChatMessage: Identifiable {
    let id = UUID()
    var text: String
    let isUser: Bool
    let prediction: String?
    let confidence: Double?
    let level: String?
    let isTyping: Bool
    var isStreaming: Bool
    
}
