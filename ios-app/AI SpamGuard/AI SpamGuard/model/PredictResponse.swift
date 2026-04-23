//
//  PredictResponse.swift
//  AI SpamGuard
//
//  Created by Akshay Kumar on 22/04/26.
//

import Foundation

// Response body
struct PredictResponse: Codable {
    let prediction: String
    let confidence: Double
    let level: String
}
