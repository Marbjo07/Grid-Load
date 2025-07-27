#include <iostream>
#include <vector>
#include <queue>
#include <set>

using namespace std;
typedef long long ll;

#define MINUTES (8 * 60)

int main() {
	float x;
	int n, m;
	cin >> x >> n >> m;

	vector<int> a(n);
	for (auto& e : a) cin >> e;

	vector<vector<float>> p(n, vector<float>(m));
	vector<vector<ll>> d(n, vector<ll>(m));
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cin >> p[i][j];
		}
	}
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < m; j++) {
			cin >> d[i][j];
		}
	}


	int numDays = 100;

	for (int day = 0; day < numDays; day++) {
		vector<float> remainCharge(n);
		for (auto& e : remainCharge) cin >> e;

		float rate = x / (float)n;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < MINUTES; j++) {
				cout << rate << " ";
			}
			cout << endl;
		}
		cout << flush;
	}

}
