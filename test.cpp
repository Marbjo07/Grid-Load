#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    const int MINUTES = 8 * 60;

    float x;
    int n, m_unused;
    cin >> x >> n >> m_unused;  
    // skip reading 'a', 'p', 'd' since they are in the generator input, not in the interactive phase
    vector<int> a(n);
    for(auto &ai : a) cin >> ai;
    // read and discard p and d
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m_unused; j++){
            float tmp; cin >> tmp;
        }
    }
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m_unused; j++){
            int tmp; cin >> tmp;
        }
    }

    // Now interactive loop:
    vector<float> remain(n);
    while (cin >> remain[0]) {
        // read the rest of remainCharge
        for(int i = 1; i < n; i++){
            cin >> remain[i];
        }

        // Your heuristic: for example, split x evenly across n stations each minute
        float rate = x / n;

        // Output n lines of MINUTES values each
        for(int i = 0; i < n; i++){
            for(int t = 0; t < MINUTES; t++){
                cout << rate;
                if (t+1 < MINUTES) cout << ' ';
            }
            cout << "\n";
        }
        // **Flush** so the grader sees your output
        cout << flush;
    }

    return 0;
}

