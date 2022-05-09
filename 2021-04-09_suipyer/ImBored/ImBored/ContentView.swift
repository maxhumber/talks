//
//  ContentView.swift
//  ImBored
//
//  Created by max on 2021-04-09.
//

import SwiftUI

struct ContentView: View {
    @StateObject var viewModel = ViewModel()
    
    var body: some View {
        VStack(spacing: 20) {
            Text("I'm Board...")
                .font(.largeTitle)
            Stepper(
                "Time: \(viewModel.game.time)",
                value: $viewModel.game.time, in: 5...120, step: 5)
            Stepper(
                "Age: \(viewModel.game.age)",
                value: $viewModel.game.age, in: 4...20, step: 4)
            HStack(spacing: 10) {
                Text("Complexity")
                Slider(value: $viewModel.game.complexity, in: 0...5)
            }
            Picker("Category", selection: $viewModel.game.category) {
                ForEach(Game.Category.allCases, id: \.self) { category in
                    Text(category.rawValue)
                }
            }
            if let prediction = viewModel.prediction {
                Text("\(prediction)")
            }
            Spacer()
        }
        .padding()
        .onAppear(perform: viewModel.predict)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
