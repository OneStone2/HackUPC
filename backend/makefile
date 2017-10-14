bin: bin/flight_planner.o
	make bin/flight_planner.o
bin/flight_planner.o: flight_planner.cpp
	g++ -Wall flight_planner.cpp -o bin/flight_planner.o

clean:
	rm bin/flight_planner.o

test:
	g++ -Wall -g flight_planner.cpp -o flight_planner.o

