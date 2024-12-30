#include <iostream>
#include <vector>
#include <cmath>
#include <ctime>
#include <cstdlib>
#include <limits>
#include <algorithm>
#include <chrono> 

using namespace std;
using namespace chrono;

class TSP {
private:
    int numVertices;
    vector<pair<int, int>> points;  // Stores points (x, y)
    vector<vector<double>> dist;    // Distance matrix

public:
    TSP(int n) : numVertices(n) {
        srand(time(0));  // Initialize random seed
        generateRandomPoints();
        calculateDistances();
    }

    void generateRandomPoints() {
        points.clear();
        for (int i = 0; i < numVertices; i++) {
            int x = rand() % 751 + 50;  // x between 50 and 750
            int y = rand() % 551 + 50;  // y between 50 and 550
            points.push_back({x, y});
        }
    }

    void calculateDistances() {
        dist.resize(numVertices, vector<double>(numVertices, 0));
        for (int i = 0; i < numVertices; i++) {
            for (int j = i + 1; j < numVertices; j++) {
                double distance = sqrt(pow(points[i].first - points[j].first, 2) +
                                       pow(points[i].second - points[j].second, 2));
                dist[i][j] = dist[j][i] = distance;
            }
        }
    }

    void printGraph() {
        cout << "\nGraph with vertices and edges (with weights):\n";
        for (int i = 0; i < numVertices; i++) {
            cout << "Vertex " << i << " (" << points[i].first << ", " << points[i].second << ")\n";
        }
        cout << "\nEdges and their weights:\n";
        for (int i = 0; i < numVertices; i++) {
            for (int j = i + 1; j < numVertices; j++) {
                cout << "Edge (" << i << ", " << j << ") - Weight: " << dist[i][j] << endl;
            }
        }
    }

    double distance(int i, int j) {
        return dist[i][j];
    }

    // Nearest Neighbor Algorithm
    void nearestNeighbor() {
        clock_t start_time = clock();
        time_t start_time_t = time(0);



        vector<bool> visited(numVertices, false);
        vector<int> path;
        int start = rand() % numVertices;
        path.push_back(start);
        visited[start] = true;
        double totalWeight = 0;

        int current = start;
        while (path.size() < numVertices) {
            double nearestDist = numeric_limits<double>::infinity();
            int nearest = -1;

            for (int i = 0; i < numVertices; i++) {
                if (!visited[i] && dist[current][i] < nearestDist) {
                    nearestDist = dist[current][i];
                    nearest = i;
                }
            }

            visited[nearest] = true;
            path.push_back(nearest);
            totalWeight += nearestDist;
            current = nearest;
        }

        // Return to the start vertex
        totalWeight += dist[current][start];
        path.push_back(start);

        cout << "\nNearest Neighbor Algorithm Result:\n";
        for (int v : path) {
            cout << "Vertex " << v << " ";
        
        }
        cout << "\nTotal Weight: " << totalWeight << endl;
        clock_t end_time = clock();  // End timer
        time_t end_time_t = time(0); // End system time


        double duration = double(end_time - start_time) / CLOCKS_PER_SEC; 
          cout << "Execution Time: " << duration << " seconds\n";  // Print the time in seconds
    }

    // Nearest Insertion Algorithm
    void nearestInsertion() {
        
        clock_t start_time = clock();
        time_t start_time_t = time(0);

        vector<pair<int, int>> cycle;
        vector<bool> visited(numVertices, false);

        // Start with the smallest edge
        double minDist = numeric_limits<double>::infinity();
        int start1 = -1, start2 = -1;
        for (int i = 0; i < numVertices; i++) {
            for (int j = i + 1; j < numVertices; j++) {
                if (dist[i][j] < minDist) {
                    minDist = dist[i][j];
                    start1 = i;
                    start2 = j;
                }
            }
        }

        visited[start1] = visited[start2] = true;
        cycle.push_back({start1, start2});
        double totalWeight = minDist;

        while (cycle.size() < numVertices) {
            double minIncrease = numeric_limits<double>::infinity();
            int insertPos = -1, vertexToInsert = -1;

            for (int v = 0; v < numVertices; v++) {
                if (!visited[v]) {
                    for (int i = 0; i < cycle.size(); i++) {
                        int u = cycle[i].first;
                        int w = cycle[i].second;
                        double increase = dist[u][v] + dist[v][w] - dist[u][w];
                        if (increase < minIncrease) {
                            minIncrease = increase;
                            vertexToInsert = v;
                            insertPos = i;
                        }
                    }
                }
            }

            visited[vertexToInsert] = true;
            cycle.push_back({cycle[insertPos].first, vertexToInsert});
            cycle.push_back({vertexToInsert, cycle[insertPos].second});
            totalWeight += minIncrease;
        }


        cout << "\nNearest Insertion Algorithm Result:\n";
        for (auto& pair : cycle) {
            cout << "Vertex " << pair.first << " -> Vertex " << pair.second << " ";
        }
        cout << "\nTotal Weight: " << totalWeight << endl;

        clock_t end_time = clock();  // End timer
        time_t end_time_t = time(0); // End system time
        cout << "End Time (BF): " << ctime(&end_time_t);  // Display end time

        double duration = double(end_time - start_time) / CLOCKS_PER_SEC; 
        cout << "Execution Time: " << duration << " seconds\n";  // Print the time in seconds
    }

    // Brute Force Algorithm
    void bruteForce() {
       
        clock_t start_time = clock();
        time_t start_time_t = time(0);
        
        double minWeight = numeric_limits<double>::infinity();
        vector<int> bestPath;

        vector<int> vertices;
        for (int i = 0; i < numVertices; i++) {
            vertices.push_back(i);
        }

        // Remove the starting vertex (assumed 0)
        vertices.erase(vertices.begin());
        do {
            double totalWeight = 0;
            vector<int> path = {0};

            for (int i = 0; i < vertices.size(); i++) {
                path.push_back(vertices[i]);
            }
            path.push_back(0);

            // Calculate total weight of the path
            for (int i = 0; i < path.size() - 1; i++) {
                totalWeight += dist[path[i]][path[i + 1]];
            }

            if (totalWeight < minWeight) {
                minWeight = totalWeight;
                bestPath = path;
            }
        } while (next_permutation(vertices.begin(), vertices.end()));


        cout << "\nBrute Force Algorithm Result:\n";
        for (int v : bestPath) {
            cout << "Vertex " << v << " ";
        }
        cout << "\nTotal Weight: " << minWeight << endl;
        clock_t end_time = clock();  // End timer
        time_t end_time_t = time(0); // End system time
        double duration = double(end_time - start_time) / CLOCKS_PER_SEC; 
        cout << "Execution Time: " << duration << " seconds\n";  // Print the time in seconds

    }
};

int main() {
    int numVertices = 20; // Number of vertices, can be changed
    TSP tsp(numVertices);

    // Generate random graph
    tsp.generateRandomPoints();
    tsp.calculateDistances();
    tsp.printGraph();

    int choice;
    bool running = true;

    while (running) {
        cout << "\nChoose an algorithm to run:\n";
        cout << "1. Nearest Neighbor Algorithm\n";
        cout << "2. Nearest Insertion Algorithm\n";
        cout << "3. Brute Force Algorithm\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                tsp.nearestNeighbor();
                break;
            case 2:
                tsp.nearestInsertion();
                break;
            case 3:
                tsp.bruteForce();
                break;
            case 4:
                running = false;
                cout << "Exiting program.\n";
                break;
            default:
                cout << "Invalid choice. Please try again.\n";
        }
    }

    return 0;
}
