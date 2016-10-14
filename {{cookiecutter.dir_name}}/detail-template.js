            Restangular.one('&app&/&l&&plural&', $routeParams.&l&ID).get().then(function(data) {
                $scope.&l& = data;
            });
