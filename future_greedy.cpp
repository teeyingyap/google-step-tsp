#include <iostream>
#include <cstdlib>
#include <cstdio> //c standard input output (for printf)
#include <vector>
#include <set>
#include <string>
#include <fstream>
#include <math.h>
#include <sys/time.h>
#include <mutex>
#include <future>
#include <algorithm>
using namespace std;


struct City
{
	double x;
	double y;
};

int N;
int num_of_threads;
double* dist = NULL;
vector <int> tour;
mutex mylock;

void load_cities(char *filename, vector<City>& cities);
double distance(City& city1, City& city2);
vector <int> solve(vector <City>& cities);
double path_length(vector <int> tour, vector <City>& cities);
bool hasShorterPath(vector <int> tour, int a, int b, int c, int d, double* dist);
vector <int> two_opt(vector <int> tour, double* dist);
vector <int> two_opt_swap(vector <int> tour, int i, int j);


double get_time()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + tv.tv_usec * 1e-6;
}



// step 1: divide tour into k segments 
// step 2: pass each segment into a thread
// step 3: do two-opt for each segment
// step 4: connect the segments together to get the final improved tour 

vector<int> two_opt_segment(int ***data, vector<int> startEnd)
{
  int segment_size = startEnd[1] - startEnd[0];
  vector<int> segment(segment_size);
  // printf("starting index = %d\n", indexList[0]);
  // printf("ending index = %d\n", indexList[1]);

  generate(segment.begin(), segment.end(), [k = startEnd[0]]() mutable { return tour[k++]; });

  int iteration = 0;
  int a, b, c, d;
  // printf("segment_size is %d\n", segment_size);
  
  while (iteration < 100)
  {
    // mutex protect a section of code allowing one thread in and blocking access to all others
    lock_guard<mutex> lock(mylock);
    for (int i = 0; i < segment_size; i++)
    {
      a = i;
      b = (i + 1) % segment_size;
      for (int j = i + 2; j < segment_size; j++)
      {
        if ((j + 1) % segment_size == i)
          continue;
        c = j % segment_size;
        d = (j + 1) % segment_size;
        if (hasShorterPath(segment, a, b, c, d, dist))
          segment = two_opt_swap(segment, i + 1, j);
      }
    }
    iteration++;
  }

  return segment;
}




int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    cout << "Usage ./a.out csv_file thread_number\n";
    return 1;
  }
  num_of_threads = atoi(argv[2]);
  char input_num = argv[1][6];
  switch(input_num) 
  {
    case '0': N = 5;
    break;
    case '1': N = 8;
    break;
    case '2': N = 16;
    break;
    case '3': N = 64;
    break;
    case '4': N = 128;
    break;
    case '5': N = 512;
    break;
    case '6': N = 2048;
    break;
    case '7': N = 8192;
    break;
    default: return 0;
  }
  vector<City> cities(N);
  load_cities(argv[1], cities);

  double begin = get_time();
  tour = solve(cities);


  // a vector of future vectors
  vector< future< vector<int> > > futures;

  int num_of_items = N / num_of_threads;
  for (int i = 0; i < num_of_threads; i++)
  {
    int start = i * num_of_items;
    int end = start + num_of_items;
    // printf("start is %d\n", start);
    // printf("end is %d\n", end);
    // fut stores the value returned by function object
    // launch::async = passed function will be executed in separate threads.
    future<vector<int> > fut = async(launch::async, two_opt_segment, nullptr, vector<int>{start, end});
    // cannot copy futures 
    // therefore "transfer" future without making a copy using move
    futures.push_back(move(fut));      
  }

  vector<int> final_tour;
  //Iterate through in the order the future was created
  // use reference &
  for (future<vector<int> >& fut : futures)
  {
    //Get the segment returned from thread
    vector<int> improved_segment = fut.get();
    //combine the segments
    final_tour.insert(final_tour.end(), improved_segment.begin(), improved_segment.end());
  }
  
  for (int i = 0; i < N; i++)
  {
    printf("%d\n", final_tour[i]);
  }
  printf("%f\n", path_length(final_tour, cities));


  double end = get_time();
  
  printf("time: %.6lf sec\n", end - begin);

  delete [] dist;  // When done, free memory pointed to by dist.
  dist = NULL;     // Clear dist to prevent using invalid memory reference.

  // ofstream csv_file("output_7.csv"); 
  // csv_file << "index" << endl;
  // for (int i = 0; i < N; i++)
  // {
  //   csv_file << tour[i] << endl;
  // }
  // csv_file.close(); 
  return 0;
}



void load_cities(char *filename, vector<City>& cities)
{
  ifstream file (filename);
  string x;
  string y;
  int k = 0;
  getline(file, x); // skip the first line
  while (getline(file, x, ','))
  {
    cities[k].x = stod(x);
    getline(file, y, '\n');
    cities[k].y = stod(y);
    k++;
  }

}

double distance(City& city1, City& city2)
{
  return sqrt(pow((city1.x - city2.x), 2) + pow((city1.y - city2.y), 2));
}

double path_length(vector <int> tour, vector <City>& cities)
{
  double sum = 0.0;
  for (int i = 0; i < N; i++)
  {
    sum += distance(cities[tour[i]], cities[tour[(i + 1) % N]]);
  }
  return sum;
}

vector <int> solve(vector <City>& cities)
{
  // double dist[N][N]; // this causes seg fault when N is too large
  // allocate on the heap
  dist =  new double[N * N]; // Pointer to double // allocate N*N doubles and save ptr in dist.
  for (int i = 0; i < N; i++) 
  {
    for (int j = 0; j < N; j++) 
    {
      dist[i * N + j] = distance(cities[i], cities[j]); // dist[i][j]
    }
  }

  int current_city = 0;
  int next_city;

  vector <int> tour = {current_city};
  // use set instead of vector so that i can remove an element from set by value
  set <int> unvisited_cities;

  for (int i = 1; i < N; i++)
  {
    unvisited_cities.insert(i);
  }

  while (!unvisited_cities.empty())
  {
    double current_dist;
    int next_city = *unvisited_cities.begin();
    double min_dist = dist[current_city * N + next_city];
    for (set<int>::iterator it = next(unvisited_cities.begin()); it != unvisited_cities.end(); it++)
    {
      int unvisited_city_index = *it;
      current_dist = dist[current_city * N + unvisited_city_index];
      if (current_dist < min_dist)
      {
        min_dist = current_dist;
        next_city = unvisited_city_index;
      }
    }
    unvisited_cities.erase(next_city);
    tour.push_back(next_city);
    current_city = next_city;

  }
  // tour = two_opt(tour, dist);
  return tour;
}


bool hasShorterPath(vector <int> tour, int a, int b, int c, int d, double* dist)
{
  if ((dist[tour[a] * N + tour[b]] + dist[tour[c] * N + tour[d]]) > (dist[tour[a] * N + tour[c]]+ dist[tour[b] * N + tour[d]]))
    return true;
  return false;
}

vector <int> two_opt_swap(vector <int> tour, int i, int j)
{
  int temp;
  while (j - i > 0)
  {
    temp = tour[i];
    tour[i] = tour[j];
    tour[j] = temp;
    i++;
    j--;
  }
  return tour;
}