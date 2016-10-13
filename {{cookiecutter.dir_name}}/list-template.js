            $scope.go = function(id) {
                $location.path('/&l&s/' + id);;
            };

            //uncomment if ordering filter is implemented in backend
            //$scope.ordering="name";

            $scope.updateData = function(page) {
                if(!isNaN(parseInt(page))){
                    $scope.query.page = page;
                }
                //uncomment if ordering filter is implemented in backend
                //$scope.query.ordering = $scope.ordering;
                $scope.promise = Restangular.all('&app&/&l&s').getList($scope.query).then(function(data) {
                    $scope.&l&s = data;
                });
            };

            $scope.options = {
                limitSelect: true,
                pageSelect: true
            };

            $scope.query = {
                limit: 5,
                page: 1,
                //uncomment if ordering filter is implemented in backend
                //ordering: $scope.ordering,
            };

            $scope.updateData(1);
