#include <bits/stdc++.h>
using namespace std;

vector<double> sgt;
const double LARGE=1e100;

double query(int l, int r, int i, int j, int p) {
	if (i>=l and j<=r) return sgt[p];
	else if (i>=r or j<=l) return LARGE;
	else return min(query(l,r,i,(i+j)/2,p*2),query(l,r,(i+j)/2,j,p*2+1));
}

int main() {
	int n, k;
	cin >> n >> k;
	int l=1;
	while (l<k+1) l*=2;
	vector<int> req(n+1,0);
	for (int i=1;i<=n;i++) cin >> req[i];
	vector< vector< vector<double> > > g(k+1,vector<vector<double> >(n+1,vector<double>(n+1)));
	for (int d=0;d<=k;d++) {
		for (int i=0;i<=n;i++) {
			for (int j=0;j<=n;j++) cin >> g[d][i][j];
		}
	}
	vector<int> perm(n);
	double best=LARGE;
	for (int i=0;i<n;i++) perm[i]=i+1;
	do {
		vector< vector<double> > dp(n+1,vector<double>(k+1,LARGE));
		for (int i=0;i<=n;i++) {
			int a, b;
			if (i==0) a=0;
			else a=perm[i-1];
			if (i==n) b=0;
			else b=perm[i];
			
			sgt=vector<double>(l*2,LARGE);
			if (i!=0) {
				for (int d=0;d<=k;d++) sgt[l+d]=dp[i-1][d];
				for (int d=l-1;d>0;d--) sgt[d]=min(sgt[2*d],sgt[2*d+1]);
			}
			for (int d=0;d<=k;d++) {
				dp[i][d]=g[d][a][b];
				if (i!=0) dp[i][d]+=query(0,i-req[perm[i-1]]+1,0,l,1);
			}
		}
		for (int d=0;d<=k;d++) best=min(best,dp[n][d]);
	} while (next_permutation(perm.begin(),perm.end()));
	cout << best << endl;
}
