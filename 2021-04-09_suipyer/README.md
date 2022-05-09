### The [S]wift[UI] + [Py]thon Playbook (SUIPYER)

By [@maxhumber](https://twitter.com/maxhumber)



#### Part 1 - Build the Skeleton

1. In Xcode create a New Project > **iOS** > **App**

2. Select the following options:

   - Name: **ImBoard**

   - Interface: **SwiftUI**
   - Life Cycle: **SwiftUI App**

3. Replace **`ContentView.swift`** with:

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("I'm Board...")
                .font(.largeTitle)
            Button(action: {}) {
                Text("Predict Fun!")
            }
            Spacer()
        }
        .padding()
    }
}
```

4. Create a new file, **`Game.swift`**:

```swift
import Foundation

struct Game {
    var name: String
    var time: Int
    var age: Int
    var complexity: Double
    var category: Category
    
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
```

6. Create a **`ViewModel.swift`**:

```swift
import Combine

class ViewModel: ObservableObject {
    var game = Game(
        name: "Pandemic", time: 45, age: 8, complexity: 2.41, category: .strategy
    )
}
```

7. Tweak `ContentView`:

```swift
struct ContentView: View {
    @StateObject var viewModel = ViewModel()
    
    var body: some View {
        VStack(spacing: 20) {
            Text("I'm Board...")
                .font(.largeTitle)
            Text("\(viewModel.game.name)")
            Text("\(viewModel.game.time)")
            Text("\(viewModel.game.age)")
            Text("\(viewModel.game.complexity)")
            Text("\(viewModel.game.category.rawValue)")
            Button(action: {}) {
                Text("Predict Fun!")
            }
            Spacer()
        }
        .padding()
    }
}
```

8. Swap out `Text("\(viewModel.game.name)")` for an editable `TextField`:

```swift
		TextField("Name", text: $viewModel.game.name)
```

9. Force the `game` in the `ViewModel` to be `@Published`:

```swift
    @Published var game = Game(
        name: "Pandemic", time: 45, age: 8, complexity: 2.41, category: .strategy
    )
```

10. Add `Stepper`s, `Slider`s, and `Picker`s to `ContentView`:

```swift
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
            Button(action: {}) {
                Text("Predict Fun!")
            }
            Spacer()
        }
        .padding()
    }
}
```

11. Spoof out a `predict` method (to be replaced) in `ViewModel`:

```swift
import Combine

class ViewModel: ObservableObject {
    @Published var game = Game(
        name: "Pandemic", time: 45, age: 8, complexity: 2.41, category: .strategy
    )
    @Published var prediction: Double?
    
    func predict() {
        prediction = 7.6
    }
}
```

12. Connect it to `ContentView` by replacing the empty `Button(action: {})` with:

```swiftUI
    Button(action: viewModel.predict) {
        Text("Predict Fun!")
    }
    if let prediction = viewModel.prediction {
        Text("\(prediction)")
    }
```



#### Part 2 - Build the Brain

13. Create a `venv` at the command line:

```sh
python -m venv .venv
```

14. Activate it:

```sh
source .venv/bin/activate
```

15. Install everything:

>  **scikit-learn==0.19.2** is the max supported version for this workflow right now 😭)

```sh
pip install coremltools scikit-learn==0.19.2 pandas tensorflow
```

16. Create a **`01-model.py`**:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import coremltools as ct

# load
df = pd.read_csv('data/games.csv')

# split
target = 'rating'
predictors = [
    'time', 'age', 'complexity', 'abstract',
    'childrens', 'customizable', 'family', 'party',
    'strategy', 'thematic', 'wargames'
]
y = df[target]
X = df[predictors]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# model
model = LinearRegression()
model.fit(X_train, y_train)
print(model.score(X_train, y_train), model.score(X_test, y_test))

# convert
coreml_model = ct.converters.sklearn.convert(model, predictors, target)
coreml_model.save('models/BoardGameRegressor1.mlmodel')
```

17. Train and export the Regressor at the command line:

```sh
python 01-model.py
```



#### Part 3 - Perform the Surgery

18. Drag+Drop **`BoardGameRegressor1.mlmodel`** into the Xcode Project Folder
    - ✅ Copy items if needed
    - ✅ Add to targets 
19. Add `import CoreML` to the top of **`ViewModel.swift`**
20. Replace the `predict` method in the `ViewModel` with:

```swift
func predict() {
    do {
        let model: BoardGameRegressor1 = try BoardGameRegressor1(configuration: .init())
        let pred = try model.prediction(
            time: Double(game.time),
            age: Double(game.age),
            complexity: game.complexity,
            abstract: game.category == .abstract ? 1.0 : 0.0,
            childrens: game.category == .childrens ? 1.0 : 0.0,
            customizable: game.category == .customizable ? 1.0 : 0.0,
            family: game.category == .family ? 1.0 : 0.0,
            party: game.category == .party ? 1.0 : 0.0,
            strategy: game.category == .strategy ? 1.0 : 0.0,
            thematic: game.category == .thematic ? 1.0 : 0.0,
            wargames: game.category == .wargames ? 1.0 : 0.0
        )
        self.prediction = pred.rating
    } catch {
        self.prediction = nil
    }
}
```

21. Build and Run to see if it works!



#### Part 4 - Make it Automagic

22. Add some defaults to the `Game` struct:

```swift
struct Game {
    var time: Int = 45
    var age: Int = 8
    var complexity: Double = 2.41
    var category: Category = .strategy
    
    // ...
}
```

23. Change the first couple of lines of `ViewModel` to:

```swift
    @Published var game = Game() {
        didSet { predict() }
    }
    @Published var prediction: Double?
```

24. Get rid of the `Button` in `ContentView` and add the following to the end of the `VStack`:

```swift
    .onAppear(perform: viewModel.predict)
```



#### Part 5 - Improve the Brain

21. Create a **`02-model.py`** file that uses Tensorflow:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import r2_score
import coremltools as ct

# load
df = pd.read_csv('data/games.csv')

# split
target = 'rating'
predictors = [
    'time', 'age', 'complexity', 'abstract',
    'childrens', 'customizable', 'family', 'party',
    'strategy', 'thematic', 'wargames'
]
y = df[target]
X = df[predictors]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# create
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(8, activation=tf.nn.relu),
    tf.keras.layers.Dense(4, activation=tf.nn.relu),
    tf.keras.layers.Dense(1),
])

# compile
model.compile(
    optimizer=tf.keras.optimizers.RMSprop(),
    loss=tf.keras.losses.mean_squared_error,
    metrics=tf.keras.metrics.mean_absolute_error
)

# train
model.fit(X_train, y_train, epochs=500, batch_size=32, validation_data=(X_test, y_test))

# evaluate
r2_score(y_test, model.predict(X_test).flatten())

# convert
coreml_model = ct.convert(model)
coreml_model.save('models/BoardGameRegressor2.mlmodel')
```

22. Run at the command line:

```sh
python 02-model.py
```



#### Part 6 - Surgery, Again

23. Drag+Drop **`BoardGameRegressor2.mlmodel`** into the Xcode Project Folder

- ✅ Copy items if needed
- ✅ Add to targets 

24. Update the `predict` method in the `ViewModel` to match:

> Note: shape: [1, 11] comes from the number of column/features

```swift
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
```

25. Build and Run!  🎉