#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

enum class MediaFormat { DVD, CD, Video };

const char* formatName(MediaFormat format) {
    switch (format) {
        case MediaFormat::DVD: return "DVD";
        case MediaFormat::CD: return "CD";
        case MediaFormat::Video: return "Video";
    }
    return "?";
}

class Date {
    int day;
    int month;
    int year;

public:
    Date(int d, int m, int y) : day(1), month(1), year(2000) {
        if (isValid(d, m, y)) {
            day = d;
            month = m;
            year = y;
        }
    }

    static bool isLeap(int y) { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }

    static int daysInMonth(int m, int y) {
        const int days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if (m == 2 && isLeap(y)) return 29;
        return days[m - 1];
    }

    static bool isValid(int d, int m, int y) {
        if (y < 1900 || y > 2100 || m < 1 || m > 12) return false;
        return d >= 1 && d <= daysInMonth(m, y);
    }

    std::string toString() const {
        std::ostringstream out;
        out << std::setfill('0') << std::setw(2) << day << '.' << std::setw(2) << month << '.' << year;
        return out.str();
    }
};

class Item {
protected:
    std::string contentType;
    Date datePurchased;
    int itemID;
    MediaFormat mediaFormat;
    static int numberOfItems;
    double price;
    std::string title;

    Item(const std::string& type, const std::string& t, double p, MediaFormat format, const Date& date)
        : contentType(type), datePurchased(date), itemID(0), mediaFormat(format), price(0), title(t) {
            if (p >= 0) price = p;
            ++numberOfItems;
            itemID = numberOfItems;
        }

public:
    Item(const Item&) = delete;
    Item& operator=(const Item&) = delete;
    virtual ~Item() { --numberOfItems; }

    const std::string& getContentType() const { return contentType; }
    const Date& getDatePurchased() const { return datePurchased; }
    int getItemId() const { return itemID; }
    MediaFormat getMediaFormat() const { return mediaFormat; }
    static int getNumberOfItems() { return numberOfItems; }
    double getPrice() const { return price; }
    const std::string& getTitle() const { return title; }

    bool setItemId(int id) {
        if (id < 1) return false;
        itemID = id;
        return true;
    }

    virtual std::string toString() const {
        std::ostringstream out;
        out << contentType << " (" << formatName(mediaFormat) << ") titled \"" << title
            << "\" was purchased for " << std::fixed << std::setprecision(2) << price
            << " EUR on " << datePurchased.toString() << '.';
        return out.str();
    }

    virtual void play() const = 0;
};

int Item::numberOfItems = 0;

class Movie : public Item {
    double rating;

public:
    Movie(const std::string& t, double p, MediaFormat format, const Date& date, double r)
        : Item("Movie", t, p, format, date), rating(0) {
            if (r >= 0 && r <= 10) rating = r;
        }

    double getRating() const { return rating; }

    bool playOnDVD() const {
        if (mediaFormat != MediaFormat::DVD) return false;
        std::cout << "Playing movie \"" << title << "\" on a DVD player\n";
        return true;
    }

    bool playOnVideo() const {
        if (mediaFormat != MediaFormat::Video) return false;
        std::cout << "Playing movie \"" << title << "\" on a video player\n";
        return true;
    }

    std::string toString() const override {
        std::ostringstream out;
        out << Item::toString() << " Rating: " << std::fixed << std::setprecision(1) << rating << "/10.";
        return out.str();
    }

    void play() const override {
        if (!playOnDVD() && !playOnVideo()) {
            std::cout << "Movie \"" << title << "\" is on " << formatName(mediaFormat)
                << ", which can't be played (only DVD or Video)\n";
        }
    }
};

class Game : public Item {
    int difficultyLevel;
    std::string mfg;

public:
    Game(const std::string& t, double p, MediaFormat format, const Date& date, int level, const std::string& maker)
        : Item("Game", t, p, format, date), difficultyLevel(1), mfg(maker) {
            if (level >= 1 && level <= 10) difficultyLevel = level;
        }

    int getDifficultyLevel() const { return difficultyLevel; }
    const std::string& getEquipment() const { return mfg; }

    bool playOnCD() const {
        if (mediaFormat != MediaFormat::CD) return false;
        std::cout << "Playing game \"" << title << "\" from a CD on " << mfg << '\n';
        return true;
    }

    bool playOnVideo() const {
        if (mediaFormat != MediaFormat::Video) return false;
        std::cout << "Playing game \"" << title << "\" from a video cassette on " << mfg << '\n';
        return true;
    }

    std::string toString() const override {
        std::ostringstream out;
        out << Item::toString() << " Difficulty: " << difficultyLevel << "/10, equipment: " << mfg << '.';
        return out.str();
    }

    void play() const override {
        if (!playOnCD() && !playOnVideo()) {
            std::cout << "Game \"" << title << "\" is on " << formatName(mediaFormat)
                << ", which can't be played (only CD or Video)\n";
        }
    }
};

class Music : public Item {
    std::string bandOrArtist;

public:
    Music(const std::string& t, double p, MediaFormat format, const Date& date, const std::string& artist)
        : Item("Music", t, p, format, date), bandOrArtist(artist) {}

    const std::string& getBandOrArtist() const { return bandOrArtist; }

    bool playOnCD() const {
        if (mediaFormat != MediaFormat::CD) return false;
        std::cout << "Playing \"" << title << "\" by " << bandOrArtist << " on a CD player\n";
        return true;
    }

    std::string toString() const override {
        return Item::toString() + " Artist: " + bandOrArtist + '.';
    }

    void play() const override {
        if (!playOnCD()) {
            std::cout << "Music \"" << title << "\" is on " << formatName(mediaFormat)
                << ", which can't be played (only CD)\n";
        }
    }
};

const int MAX_ITEMS = 20;

class Collection {
    Item* items[MAX_ITEMS];
    int count;

public:
    Collection() : count(0) {}
    Collection(const Collection&) = delete;
    Collection& operator=(const Collection&) = delete;

    ~Collection() {
        for (int i = 0; i < count; ++i) delete items[i];
    }

    int size() const { return count; }
    bool isFull() const { return count == MAX_ITEMS; }

    Item* findById(int id) const {
        for (int i = 0; i < count; ++i) {
            if (items[i]->getItemId() == id) return items[i];
        }
        return nullptr;
    }

    int nextFreeId() const {
        int id = 1;
        while (findById(id) != nullptr) ++id;
        return id;
    }

    bool add(Item* item) {
        if (isFull()) {
            delete item;
            return false;
        }
        if (findById(item->getItemId()) != nullptr) item->setItemId(nextFreeId());
        items[count++] = item;
        return true;
    }

    const Item& at(int index) const { return *items[index]; }

    bool changeId(int oldId, int newId) {
        Item* item = findById(oldId);
        if (item == nullptr || newId < 1) return false;
        if (newId != oldId && findById(newId) != nullptr) return false;
        return item->setItemId(newId);
    }

    double totalPrice() const {
        double sum = 0;
        for (int i = 0; i < count; ++i) sum += items[i]->getPrice();
        return sum;
    }
};

void printItem(const Item& item) {
    std::cout << "#" << item.getItemId() << ' ' << item.toString() << '\n';
}

void printCollection(const Collection& collection) {
    if (collection.size() == 0) {
        std::cout << "The collection is empty\n";
        return;
    }
    for (int i = 0; i < collection.size(); ++i) printItem(collection.at(i));
    std::ostringstream total;
    total << std::fixed << std::setprecision(2) << collection.totalPrice();
    std::cout << "Items: " << Item::getNumberOfItems() << ", total value: " << total.str() << " EUR\n";
}

std::string trim(const std::string& s) {
    const std::string spaces = " \t\r\n";
    std::string::size_type first = s.find_first_not_of(spaces);
    if (first == std::string::npos) return "";
    std::string::size_type last = s.find_last_not_of(spaces);
    return s.substr(first, last - first + 1);
}

bool readLine(const std::string& prompt, std::string& value) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        line = trim(line);
        if (!line.empty()) {
            value = line;
            return true;
        }
        std::cout << "Value can't be empty: ";
    }
    return false;
}

bool readInt(const std::string& prompt, int low, int high, int& value) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        int v;
        char extra;
        if (in >> v && !(in >> extra) && v >= low && v <= high) {
            value = v;
            return true;
        }
        std::cout << "Enter a whole number from " << low << " to " << high << ": ";
    }
    return false;
}

bool readDouble(const std::string& prompt, double low, double high, double& value) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        double v;
        char extra;
        if (in >> v && !(in >> extra) && v >= low && v <= high) {
            value = v;
            return true;
        }
        std::cout << "Enter a number from " << low << " to " << high << ": ";
    }
    return false;
}

bool readDate(const std::string& prompt, Date& value) {
    std::cout << prompt;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line);
        int d;
        int m;
        int y;
        char dot1;
        char dot2;
        char extra;
        if (in >> d >> dot1 >> m >> dot2 >> y && !(in >> extra) && dot1 == '.' && dot2 == '.'
                && Date::isValid(d, m, y)) {
            value = Date(d, m, y);
            return true;
        }
        std::cout << "Enter a valid date as dd.mm.yyyy (1900-2100): ";
    }
    return false;
}

bool readFormat(MediaFormat& value) {
    int choice;
    if (!readInt("Media format (1 = DVD, 2 = CD, 3 = Video): ", 1, 3, choice)) return false;
    value = choice == 1 ? MediaFormat::DVD : (choice == 2 ? MediaFormat::CD : MediaFormat::Video);
    return true;
}

bool readCommon(std::string& title, double& price, MediaFormat& format, Date& date) {
    return readLine("Title: ", title) && readDouble("Price (EUR): ", 0, 100000, price)
        && readFormat(format) && readDate("Date purchased (dd.mm.yyyy): ", date);
}

bool addItem(Collection& collection, int type) {
    if (collection.isFull()) {
        std::cout << "The collection is full (" << MAX_ITEMS << " items)\n";
        return true;
    }
    std::string title;
    double price;
    MediaFormat format;
    Date date(1, 1, 2000);
    if (!readCommon(title, price, format, date)) return false;

    Item* item = nullptr;
    if (type == 1) {
        double rating;
        if (!readDouble("Rating (0-10): ", 0, 10, rating)) return false;
        item = new Movie(title, price, format, date, rating);
    } else if (type == 2) {
        int level;
        std::string maker;
        if (!readInt("Difficulty level (1-10): ", 1, 10, level) || !readLine("Equipment / manufacturer: ", maker)) {
            return false;
        }
        item = new Game(title, price, format, date, level, maker);
    } else {
        std::string artist;
        if (!readLine("Band or artist: ", artist)) return false;
        item = new Music(title, price, format, date, artist);
    }
    collection.add(item);
    std::cout << "Added ";
    printItem(*item);
    return true;
}

bool playItem(const Collection& collection) {
    int id;
    if (!readInt("Item ID: ", 1, 1000000, id)) return false;
    const Item* item = collection.findById(id);
    if (item == nullptr) {
        std::cout << "No item with ID " << id << '\n';
    } else {
        item->play();
    }
    return true;
}

bool changeItemId(Collection& collection) {
    int oldId;
    int newId;
    if (!readInt("Current ID: ", 1, 1000000, oldId) || !readInt("New ID: ", 1, 1000000, newId)) return false;
    if (collection.findById(oldId) == nullptr) {
        std::cout << "No item with ID " << oldId << '\n';
    } else if (!collection.changeId(oldId, newId)) {
        std::cout << "ID " << newId << " is already used\n";
    } else {
        std::cout << "ID " << oldId << " changed to " << newId << '\n';
    }
    return true;
}

int main() {
    Collection collection;
    collection.add(new Movie("Inception", 19.99, MediaFormat::DVD, Date(12, 10, 2026), 8.8));
    collection.add(new Game("Chess Master", 29.50, MediaFormat::CD, Date(3, 9, 2025), 7, "PC"));
    collection.add(new Music("Abbey Road", 15.00, MediaFormat::CD, Date(29, 2, 2024), "The Beatles"));
    collection.add(new Movie("Back to the Future", 5.00, MediaFormat::Video, Date(1, 6, 1999), 8.5));

    std::cout << "Media Collection Tool\n\n";
    printCollection(collection);
    std::cout << '\n';
    for (int i = 0; i < collection.size(); ++i) collection.at(i).play();

    bool running = true;
    while (running) {
        std::cout << "\n1 = add movie, 2 = add game, 3 = add music, 4 = list, 5 = play, 6 = change ID, 0 = exit\n";
        int choice;
        if (!readInt("Choice: ", 0, 6, choice)) break;
        switch (choice) {
            case 0:
                std::cout << "Bye\n";
                return 0;
            case 1:
            case 2:
            case 3:
                running = addItem(collection, choice);
                break;
            case 4:
                printCollection(collection);
                break;
            case 5:
                running = playItem(collection);
                break;
            case 6:
                running = changeItemId(collection);
                break;
        }
    }
    std::cout << "\nInput ended\n";

    return 0;
}
