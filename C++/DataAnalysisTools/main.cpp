#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>
#include <algorithm>

// C++ Data Analysis Tool
// Calculates Mean, Median, Mode, Standard Deviation

double calculateMean(const std::vector<double>& data) {
    double sum = std::accumulate(data.begin(), data.end(), 0.0);
    return sum / data.size();
}

double calculateMedian(std::vector<double> data) {
    std::sort(data.begin(), data.end());
    size_t n = data.size();
    if (n % 2 == 0) {
        return (data[n/2 - 1] + data[n/2]) / 2.0;
    } else {
        return data[n/2];
    }
}

double calculateStdDev(const std::vector<double>& data) {
    double mean = calculateMean(data);
    double sq_sum = 0.0;
    for (double x : data) {
        sq_sum += (x - mean) * (x - mean);
    }
    return std::sqrt(sq_sum / data.size());
}

int main() {
    std::vector<double> data;
    double input;
    
    std::cout << "--- Data Analysis Tool ---" << std::endl;
    std::cout << "Enter numbers (enter -1 to finish):" << std::endl;
    
    while (std::cin >> input && input != -1) {
        data.push_back(input);
    }
    
    if (data.empty()) {
        std::cout << "No data entered." << std::endl;
        return 0;
    }
    
    std::cout << "\n[Results]" << std::endl;
    std::cout << "Count: " << data.size() << std::endl;
    std::cout << "Mean:  " << calculateMean(data) << std::endl;
    std::cout << "Median:" << calculateMedian(data) << std::endl;
    std::cout << "StdDev:" << calculateStdDev(data) << std::endl;
    
    return 0;
}
