CXX = g++
CXXFLAGS = -std=c++17
LDFLAGS = -lxml2 -lcld2 -pthread
INCLUDES = -I/usr/include/libxml2 -I/usr/include/cld2/public
TARGET = parseXML
SRC = parseXML.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SRC) $(LDFLAGS) -o $(TARGET)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)
