#include <iostream>
#include <cstdlib>
#include <cstdio> //c standard input output (for printf)
#include <vector>
#include <set>
#include <string>
#include <fstream>
#include <math.h>
#include <sys/time.h>
using namespace std;


struct City
{
	double x;
	double y;
};

int N;


void load_cities(char *filename, vector<City>& cities);
double distance(City& city1, City& city2);
vector <int> solve(vector <City>& cities);
double path_length(vector <int> tour, vector <City>& cities);
bool hasShorterPath(vector <City>& cities, vector <int> tour, int a, int b, int c, int d, double* dist);
vector <int> two_opt(vector <City>& cities, vector <int> tour, double* dist);
vector <int> two_opt_swap(vector <int> tour, int i, int j);


double get_time()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + tv.tv_usec * 1e-6;
}


int main(int argc, char *argv[])
{
  if (argc != 2)
  {
    cout << "Usage ./a.out csv_file \n";
    return 1;
  }

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
  // for (int i = 0; i < N; i++)
  // {
  //   printf("x = %f ", cities[i].x);
  //   printf("y = %f\n", cities[i].y);
  // }
  double begin = get_time();
  vector <int> tour = solve(cities);
  double end = get_time();
  

  for (int i = 0; i < N; i++)
  {
    printf("%d ", tour[i]);
    printf("\n");
  }
  printf("time: %.6lf sec\n", end - begin);
  printf("%f\n", path_length(tour, cities));
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
    // cout << "x: " << x << " " ;
    getline(file, y, '\n');
    cities[k].y = stod(y);
    // cout << "y: " << y << " " ;
    // cout << "\n";
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
  // double dist[N][N]; // this causes seg fault
  // allocate on the heap
  double* dist =  new double[N * N]; // Pointer to double // allocate N*N doubles and save ptr in dist.
  // double (*dist)[N] = new int[N][N];
  for (int i = 0; i < N; i++) 
  {
    for (int j = 0; j < N; j++) 
    {
      dist[i * N + j] = distance(cities[i], cities[j]); // dist[i][j]
    }
  }
  // printf("HI\n");

  // for (int i = 0; i < N; i++)
  // {
  //   for (int j = 0; j < N; j++)
  //   {
  //     printf("%d and %d is %f\n", i, j, dist[i][j]);
  //   }
  // }
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
  tour = two_opt(cities, tour, dist);
  delete [] dist;  // When done, free memory pointed to by dist.
  dist = NULL;     // Clear dist to prevent using invalid memory reference.
  return tour;
}


vector <int> two_opt(vector <City>& cities, vector <int> tour, double* dist)
{
  int iteration = 0;
  int a, b, c, d;
  while (iteration < 100)
  {
    for (int i = 0; i < N; i++)
    {
      a = i;
      b = (i + 1) % N;
      for (int j = i + 2; j < N; j++)
      {
        if ((j + 1) % N == i)
          continue;
        c = j % N;
        d = (j + 1) % N;
        if (hasShorterPath(cities, tour, a, b, c, d, dist))
          tour = two_opt_swap(tour, i + 1, j);
      }
    }
    iteration++;
  }
  return tour;
}


bool hasShorterPath(vector <City>& cities, vector <int> tour, int a, int b, int c, int d, double* dist)
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