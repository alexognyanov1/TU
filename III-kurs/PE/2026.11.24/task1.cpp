#include <iostream>
#include <sstream>
#include <string>

const double minSide = 0.01;
const double maxSide = 1000.0;
const double maxVolume = 1000000000.0;

class CBox {
public:
    CBox(double lv = 1.0, double wv = 1.0, double hv = 1.0) : m_Height(hv) {
        m_Length = lv > wv ? lv : wv;
        m_Width = wv < lv ? wv : lv;
    }

    double Volume() const {
        return m_Length * m_Width * m_Height;
    }

    int operator>(const CBox& aBox) const {
        return this->Volume() > aBox.Volume();
    }

    int operator>(const double& value) const {
        return Volume() > value;
    }

    int operator<(const CBox& aBox) const {
        return this->Volume() < aBox.Volume();
    }

    int operator<(const double& value) const {
        return Volume() < value;
    }

    int operator==(const CBox& aBox) const {
        return this->Volume() == aBox.Volume();
    }

    int operator==(const double& value) const {
        return Volume() == value;
    }

    CBox operator+(const CBox& aBox) const {
        return CBox(m_Length > aBox.m_Length ? m_Length : aBox.m_Length,
                m_Width > aBox.m_Width ? m_Width : aBox.m_Width,
                m_Height + aBox.m_Height);
    }

    CBox operator-(const CBox& aBox) const {
        double height = m_Height - aBox.m_Height;
        return CBox(m_Length, m_Width, height > 0.0 ? height : 0.0);
    }

    void ShowBox() const {
        std::cout << m_Length << " " << m_Width << " " << m_Height << std::endl;
    }

private:
    double m_Length;
    double m_Width;
    double m_Height;
};

int operator>(const double& value, const CBox& aBox) {
    return value > aBox.Volume();
}

int operator<(const double& value, const CBox& aBox) {
    return value < aBox.Volume();
}

int operator==(const double& value, const CBox& aBox) {
    return value == aBox.Volume();
}

const char* answer(int result) {
    return result ? "yes" : "no";
}

void show(const std::string& name, const CBox& box) {
    std::cout << name << " dimensions are ";
    box.ShowBox();
}

void compare(const std::string& leftName, const CBox& left, const std::string& rightName, const CBox& right) {
    std::cout << leftName << " < " << rightName << ": " << answer(left < right) << '\n';
    std::cout << leftName << " == " << rightName << ": " << answer(left == right) << '\n';
    std::cout << leftName << " > " << rightName << ": " << answer(left > right) << '\n';
}

void compare(const std::string& name, const CBox& box, double value) {
    std::cout << name << " < " << value << ": " << answer(box < value) << '\n';
    std::cout << name << " == " << value << ": " << answer(box == value) << '\n';
    std::cout << value << " < " << name << ": " << answer(value < box) << '\n';
    std::cout << value << " == " << name << ": " << answer(value == box) << '\n';
}

bool readNumbers(const std::string& prompt, int count, double low, double high, double values[]) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        bool valid = true;
        for (int i = 0; i < count && valid; ++i) {
            valid = (in >> values[i]) && values[i] >= low && values[i] <= high;
        }
        std::string extra;
        if (valid && !(in >> extra)) {
            return true;
        }
        std::cout << "Enter " << count << (count == 1 ? " number" : " numbers") << " from " << low << " to " << high << ": ";
    }
    return false;
}

bool readBox(const std::string& name, CBox& box) {
    double sides[3];
    if (!readNumbers(name + " (length width height): ", 3, minSide, maxSide, sides)) {
        return false;
    }
    box = CBox(sides[0], sides[1], sides[2]);
    return true;
}

int main() {
    CBox smallBox(4.0, 2.0, 1.0);
    CBox mediumBox(10.0, 4.0, 2.0);
    CBox aBox;
    CBox bBox;

    std::cout << "Adding CBox objects\n";
    aBox = smallBox + mediumBox;
    std::cout << "aBox dimensions are ";
    aBox.ShowBox();

    bBox = aBox + smallBox + mediumBox;
    std::cout << "bBox dimensions are ";
    bBox.ShowBox();

    std::cout << "\nOperators <, == and -\n";
    show("smallBox", smallBox);
    show("mediumBox", mediumBox);
    std::cout << "smallBox volume: " << smallBox.Volume() << ", mediumBox volume: " << mediumBox.Volume() << '\n';
    compare("smallBox", smallBox, "mediumBox", mediumBox);
    compare("mediumBox", mediumBox, "smallBox", smallBox);
    compare("smallBox", smallBox, 8.0);
    compare("mediumBox", mediumBox, 100.0);

    CBox cBox = aBox - smallBox;
    show("aBox - smallBox", cBox);
    std::cout << "aBox - smallBox == mediumBox: " << answer(cBox == mediumBox) << '\n';
    show("bBox - aBox - smallBox", bBox - aBox - smallBox);
    show("smallBox - mediumBox", smallBox - mediumBox);
    std::cout << "smallBox - mediumBox == 0: " << answer(smallBox - mediumBox == 0.0) << '\n';

    std::cout << "\nYour boxes (sides from " << minSide << " to " << maxSide << ")\n";
    CBox first;
    CBox second;
    double value[1];
    if (!readBox("Box A", first) || !readBox("Box B", second)
            || !readNumbers("Volume to compare with: ", 1, 0.0, maxVolume, value)) {
        std::cout << "\nInput ended\n";
        return 0;
    }

    show("A", first);
    show("B", second);
    std::cout << "A volume: " << first.Volume() << ", B volume: " << second.Volume() << '\n';
    compare("A", first, "B", second);
    compare("A", first, value[0]);
    compare("B", second, value[0]);
    show("A + B", first + second);
    show("A - B", first - second);
    show("B - A", second - first);
    std::cout << "A + B - B == A: " << answer(first + second - second == first) << '\n';
    return 0;
}
