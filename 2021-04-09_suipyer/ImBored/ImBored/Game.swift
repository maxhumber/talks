//
//  Game.swift
//  ImBored
//
//  Created by max on 2021-04-09.
//

import Foundation

struct Game {
    var time: Int = 45
    var age: Int = 8
    var complexity: Double = 2.41
    var category: Category = .strategy
    
    enum Category: String, CaseIterable {
        case abstract = "Abstract"
        case childrens = "Childrens"
        case customizable = "Customizable"
        case family = "Family"
        case party = "Party"
        case strategy = "Strategy"
        case thematic = "Thematic"
        case wargames = "Wargames"
    }
}
