//
//  TypingIndicatorView.swift
//  RAG Assistant
//
//  Created by Akshay Kumar on 16/04/26.
//

import SwiftUI

struct TypingIndicatorView: View {
    
    @State private var animate = false
    
    var body: some View {
        HStack(spacing: 6) {
            
            Circle()
                .frame(width: 8, height: 8)
                .scaleEffect(animate ? 1 : 0.5)
                .offset(y: animate ? -2 : 2)
                .animation(.easeInOut(duration: 0.6).repeatForever().delay(0), value: animate)
            
            Circle()
                .frame(width: 8, height: 8)
                .scaleEffect(animate ? 1 : 0.5)
                .offset(y: animate ? -2 : 2)
                .animation(.easeInOut(duration: 0.6).repeatForever().delay(0.2), value: animate)
            
            Circle()
                .frame(width: 8, height: 8)
                .scaleEffect(animate ? 1 : 0.5)
                .offset(y: animate ? -2 : 2)
                .animation(.easeInOut(duration: 0.6).repeatForever().delay(0.4), value: animate)
        }
        .onAppear {
            animate = true
        }
    }
}

#Preview {
    TypingIndicatorView()
}
