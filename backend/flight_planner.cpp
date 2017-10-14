#include <bits/stdc++.h>
using namespace std;

vector< pair<double,int> > sgt;
const double LARGE=1e100;

pair<double,int> query(int l, int r, int i, int j, int p) {
	if (r<=l) return {LARGE,0};
	if (i>=l and j<=r) return sgt[p];
	if (i>=r or j<=l) return {LARGE,0};
	return min(query(l,r,i,(i+j)/2,p*2),query(l,r,(i+j)/2,j,p*2+1));
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
			for (int j=0;j<=n;j++) {
				cin >> g[d][i][j];
				if (g[d][i][j]==-1) g[d][i][j]=LARGE;
			}
		}
	}
	vector<int> perm(n);
	double best=LARGE;
	vector<pair<int,int> > optimal(n+1);
	for (int i=0;i<n;i++) perm[i]=i+1;
	do {
		vector< vector< pair<double,int> > > dp(n+1,vector< pair<double,int> >(k+1,{LARGE,0}));
		for (int i=0;i<=n;i++) {
			int a, b;
			if (i==0) a=0;
			else a=perm[i-1];
			if (i==n) b=0;
			else b=perm[i];
			
			sgt=vector< pair<double,int> >(l*2,{LARGE,0});
			if (i!=0) {
				for (int d=0;d<=k;d++) {
					sgt[l+d].first=dp[i-1][d].first;
					sgt[l+d].second=d;
				}
				for (int d=l-1;d>0;d--) sgt[d]=min(sgt[2*d],sgt[2*d+1]);
			}
			for (int d=0;d<=k;d++) {
				dp[i][d]={g[d][a][b],0};
				if (i!=0) {
					pair<double,int> res=query(0,d-req[perm[i-1]]+1,0,l,1);
					dp[i][d].first+=res.first;
					dp[i][d].second=res.second;
				}
			}
		}
		for (int d=0;d<=k;d++) {
			if (dp[n][d].first<best) {
				best=dp[n][d].first;
				optimal[n]={0,d};
				int cur=dp[n][d].second;
				for (int j=n-1;j>=0;j--) {
					optimal[j]={perm[j],cur};
					cur=dp[j][cur].second;
				}
			}
		}
	} while (next_permutation(perm.begin(),perm.end()));
	if (best>=LARGE) cout << "IMPOSSIBLE" << endl;
	else {
		cout << "{\"cost\":" << best << "," << endl;
		cout << "\"vols\":[" << endl;
		for (int i=0;i<=n;i++) {
			cout << "{\"dest\":" << optimal[i].first << ",\"dia\":" << optimal[i].second << "}";
			if (i!=n) cout << ",";
			cout << endl;
		}
		cout << "]}" << endl;
	}
}
