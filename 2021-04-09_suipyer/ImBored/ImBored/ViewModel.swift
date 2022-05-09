//
//  ViewModel.swift
//  ImBored
//
//  Created by max on 2021-04-09.
//

import Combine
import CoreML

class ViewModel: ObservableObject {
    @Published var game = Game() {
        didSet { predict() }
    }
    @Published var prediction: Double?
    
    func predict() {
        do {
            let mlArray = try? MLMultiArray(
                shape: [1, 11], dataType: MLMultiArrayDataType.float32
            )
            mlArray![0] = NSNumber(value: game.time)
            mlArray![1] = NSNumber(value: game.age)
            mlArray![2] = NSNumber(value: game.complexity)
            mlArray![3] = NSNumber(value: game.category == .abstract ? 1.0 : 0.0)
            mlArray![4] = NSNumber(value: game.category == .childrens ? 1.0 : 0.0)
            mlArray![5] = NSNumber(value: game.category == .customizable ? 1.0 : 0.0)
            mlArray![6] = NSNumber(value: game.category == .family ? 1.0 : 0.0)
            mlArray![7] = NSNumber(value: game.category == .party ? 1.0 : 0.0)
            mlArray![8] = NSNumber(value: game.category == .strategy ? 1.0 : 0.0)
            mlArray![9] = NSNumber(value: game.category == .thematic ? 1.0 : 0.0)
            mlArray![9] = NSNumber(value: game.category == .wargames ? 1.0 : 0.0)
            let model: BoardGameRegressor2 = try BoardGameRegressor2(configuration: .init())
            let pred = try model.prediction(input:
                BoardGameRegressor2Input(input_1: mlArray!)
            )
            self.prediction = Double(truncating: pred.Identity[0])
        } catch {
            self.prediction = nil
        }
    }
}
