#include "io\TextIO.h"
#include "field\F2.h"
#include <vector>
#include <string>
#include <iostream> // tik jei reikia debug

extern int k; // globalus k

std::vector<std::vector<F2>> stringToVectors(const std::string& text) {
    std::vector<std::vector<F2>> result;
    for (char ch : text) {
        int val = static_cast<unsigned char>(ch);
        std::vector<F2> bits(8, F2(0));
        for (int i = 7; i >= 0; --i) {
            bits[i] = F2(val % 2);
            val /= 2;
        }
        for (int i = 0; i < 8; i += k) {
            std::vector<F2> block(k, F2(0));
            for (int j = 0; j < k && i+j < 8; ++j)
                block[j] = bits[i+j];
            result.push_back(block);
        }
    }
    return result;
}

std::string vectorsToString(const std::vector<std::vector<F2>>& vectors) {
    std::string s;
    for (size_t i = 0; i < vectors.size(); i += (8/k)) {
        int val = 0;
        for (int j = 0; j < 8; ++j) {
            int blockIndex = i + j/k;
            int bitIndex = j % k;
            if (blockIndex < vectors.size())
                val = (val << 1) | vectors[blockIndex][bitIndex].v;
        }
        s += static_cast<char>(val);
    }
    return s;
}
