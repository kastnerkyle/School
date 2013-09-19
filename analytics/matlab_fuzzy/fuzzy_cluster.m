num_clusters = 5;
X = dlmread('train.csv', ',' , [1,1,500,3]);
fuzzy_centers = fcm(X, num_clusters, [25,1E-5,0]);
[unused, kmeans_centers] = kmeans(X, num_clusters)

% Data
% Normalization
mu = mean(X);
c = bsxfun(@minus, X, mu);
% Eigenvector decomposition (sorted into descending order)
covar = cov(c);
[U,S,V] = svd(covar);
reduced_X = c*V(:, 1:2);

% Kmeans clusters
% Normalization
mu = mean(kmeans_centers);
c = bsxfun(@minus, kmeans_centers, mu);
% Eigenvector decomposition (sorted into descending order)
covar = cov(c);
[U,S,V] = svd(covar);
reduced_kmeans = c*V(:, 1:2);

% Fuzzy clusters
% Normalization
mu = mean(fuzzy_centers);
c = bsxfun(@minus, fuzzy_centers, mu);
% Eigenvector decomposition (sorted into descending order)
covar = cov(c);
[U,S,V] = svd(covar);
reduced_fuzzy = c*V(:, 1:2);

%Plotting
clf
hold on
scatter(reduced_X(:,1),reduced_X(:,2),'black')
scatter(reduced_fuzzy(:,1),reduced_fuzzy(:,2),'red')
scatter(reduced_kmeans(:,1),reduced_kmeans(:,2),'blue')
%Scatter legend is bugged in my version.
%Sigh
%http://savannah.gnu.org/bugs/?33463
legend({'data', 'fuzzy','kmeans'});
legend('show')
print -dpng kyle_base.png
hold off	