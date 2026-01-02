#include <iostream>
#include <vector>
#include <numeric>

// C++ Perceptron (Simple Neural Network)

class Perceptron {
    std::vector<double> weights;
    double bias;
    double learningRate;

public:
    Perceptron(int inputs, double lr) : bias(0.0), learningRate(lr) {
        for(int i=0; i<inputs; i++) weights.push_back(0.0);
    }

    int predict(const std::vector<double>& inputs) {
        double sum = bias;
        for(size_t i=0; i<inputs.size(); i++) {
            sum += inputs[i] * weights[i];
        }
        return (sum > 0) ? 1 : 0; // Activation Function (Step)
    }

    void train(const std::vector<std::vector<double>>& trainingInputs, const std::vector<int>& labels, int epochs) {
        for(int epoch=0; epoch<epochs; epoch++) {
            int errors = 0;
            for(size_t i=0; i<trainingInputs.size(); i++) {
                int prediction = predict(trainingInputs[i]);
                int error = labels[i] - prediction;
                
                if(error != 0) {
                    errors++;
                    bias += learningRate * error;
                    for(size_t j=0; j<weights.size(); j++) {
                        weights[j] += learningRate * error * trainingInputs[i][j];
                    }
                }
            }
            if(epoch % 10 == 0)
                std::cout << "Epoch " << epoch << " Errors: " << errors << std::endl;
        }
    }
};

int main() {
    std::cout << "--- C++ Perceptron (OR Gate) ---" << std::endl;
    
    // OR Gate Data
    std::vector<std::vector<double>> inputs = {
        {0, 0},
        {0, 1},
        {1, 0},
        {1, 1}
    };
    std::vector<int> targets = {0, 1, 1, 1}; // OR logic
    
    Perceptron p(2, 0.1);
    
    std::cout << "Training..." << std::endl;
    p.train(inputs, targets, 50);
    
    std::cout << "\nTesting:" << std::endl;
    std::cout << "0 OR 0 = " << p.predict({0, 0}) << std::endl;
    std::cout << "0 OR 1 = " << p.predict({0, 1}) << std::endl;
    std::cout << "1 OR 0 = " << p.predict({1, 0}) << std::endl;
    std::cout << "1 OR 1 = " << p.predict({1, 1}) << std::endl;
    
    return 0;
}
